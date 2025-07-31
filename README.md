The purpose of the app is to represent the public IP of the computer that
the app runs on. In order to achieve this I created the app using python.
Then I wrote a Dockerfile for the app and ran it locally. Then I created a 
version control repository for the project using github. 
I decided to create the infrastructure for the project using AWS cloud.
I chose to work with jenkins as a CI tool. In order two achive this in AWS 
I deployed two instances in public subnet in a VPC that I created. The first one
is a Jenkins Controller node which is responsible to process the Jenkisfile.
The second one is the jenkins slave which provides the workload to run the
Jenkinsfile. 
After I installed Jenkins on the controller node, I didn't succeed to run jobs
on it and I discovered it happened because there wasn't enough space in /tmp.
In order to solve it I reformat it's file system and then it worked.
When I finished deploying the infrastructure needed for the project, I created
job in jenkins that commits the pipeline. I defined it to run on the jenkins
slave and allowed it to be triggered from GIT hooks. I created webhook in 
my repository so every time changes are pushed to the repo it will trigger a
new build in the pipeline.
The CI process itself checks that the slave has required dependencies.
Then it builds a docker image, scans it using a tool named trivy and exports
reports which contains severities of HIGH and CRITICAL to HTML and XML files.
Then the image is pushed to repository in docker hub. I used the GIT_COMMIT
environemt variable to give each image a unique name.
The testing stage includes unit and integration tests of the python application.
The unit tests checks that the api endpoints I defined in my Flask application
works as they should. If one of them returns an error, the build will fail.
For the deployment to work, I created a single-node kubernetes cluster on my
jenkins slave. Then, inside the Jenkinsfile I installed helm and deployed 
ingress-nginx controller using helm chart for ingresses to work in my cluster.
I defined the controller service to be from a NodePort type because I my k8s
cluster is not managed as a cloud service so I can't install load balancer 
controller and services from the load balancer type won't do anything.
Then I deployed my helm chart to the cluster. It contains 4 files for k8s api objects
and values file as well.
As post stages I made the HTML and XML reports from the trivy tool accessible outside of 
the workspace of the build in jenkins. I also send email notification to my gmail account
every time a build is complete.

Challenges along the way:
I installed email extension and email extension template plugins. 

