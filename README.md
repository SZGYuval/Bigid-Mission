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
