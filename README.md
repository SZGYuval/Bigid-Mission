**Project Overview:**
* Language & Framework: Python + Flask
* Infrastructure: AWS EC2, custom VPC
* Containerization & Deployment: Docker, K8S, Helm
* CI/CD: Jenkins
* Security Scanning: Trivy
* Testing: Unit and Integration Tests
* Reporting: HTML & XML vulnerability reports
* Notifications: Email alerts via Gmail

**Application:**
* A simple Flask application that exposes endpoints to fetch the machine's public IP.
  
**Architecture:**
* AWS cloud based Infrastructure
* VPC
* Internet Gateway
* 2 public subnets
* 2 private subnets

**Version Control:**
* Project is version-controlled using GitHub.
* Webhooks are configured to trigger Jenkins jobs on every git push.

**Servers:**
* Two EC2 Instances:
* Jenkins Controller: Handles the Jenkins UI.
* Jenkins Agent (Slave): Executes the Jenkins pipelines.

**CI/CD Pipeline (via Jenkins)**
Trigger:
Webhook triggers the Jenkins pipeline on every push to the GitHub repository.

**Pipeline Stages:**
1- Ensure required dependencies are installed on the Jenkins slave.

2- Build:
 * Docker image is built from the application code.
 * Image is scanned using Trivy.
 * Reports with vulnerabilities of HIGH and CRITICAL severities are exported in HTML and XML formats.
 * The built image is pushed to Docker Hub.

3- Testing:
 * Unit Tests: Validate Flask API endpoints.
 * Integration Tests: Ensure the application functions correctly in its environment.

4- Deployment:
 * Helm and Ingress-NGINX Controller are installed (via Helm).
 * Since the Kubernetes cluster is self-managed, the Ingress Controller service is configured as NodePort.
 The Helm chart for the app includes:
 *   Deployment
 *   Service
 *   Ingress
 *   Namespace
values.yaml

5- Post Actions:
 * Trivy reports are made accessible outside of Jenkins workspace.
 * Email notification is sent upon completion of each build.

**Challenges along the way**

1- When configuring jenkins the nodes where offline. I found out it happened 
because there wasn't enough space left in /tmp directory so I had to resize it.

2- When deploying the helm chart to my K8S cluster. The pods were evicted from
the node. I checked the logs using the describe command and saw alert on disk
pressure on the node. In order to solve it I resized the EBS volume.

3- When I configured the pipeline to send emails, at first I just configured
settings in the email plugin and when I tested the connection it worked but
when I ran the pipeline and it still didn't work. I then discovered that I 
need to configure the same settings in the email extension plugin as well.

4- In order to configure certificate for the jenkins website, I used ALB. I 
deployed the ALB and created dns record in my domain in order to create the
certificate. I also created the target group and defined the /health to be
on port 8080. After the load balancer was created I saw that the health check
fails and I get 403 html error code. I realized that in order for it to work
I need to allow anonymous read only. After allowing it the health check didn't
failed but then I could log in to the jenkins website with the load balancer
url without entering any credentials as anonymous. After further investigation,
I discovered that jenkins has the /login api endpoint which does not require 
authentication, so I changed the health check path to /login. Then everything
worked as expected without selecting "the allow anonymous read access" option.

5- For pushing the docker image to docker hub I first needed to login to docker
hub with my credentials. In order to so, I created credentials object containing
my docker hub account details within jenkins credentials section. I also installed
the docker pipepline plugin and then I genereted a groovy command to push the image
which authenticates with the docker hub credentials object as well.

6- I had some problems with installing the trivy tool because both ways that 
were offered according to trivy official website didn't work as expected. At
first I tried to add the repo and it didn't find the url of it when I used the
yum upgrade command. I then installed using the rpm directly. At first, I 
thought it worked because and I succeeded to generate reports but then I saw
that the trivy convert command is not installed. I searched for another trivy 
installation. In the end I found suitable installation which answered all my
requirements.

7- I also installed certificate to my ingress controller. In order to do so,
I used cert-manager in my cluster.