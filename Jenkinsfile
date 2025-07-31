pipeline {
    agent { label 'aws-slave-node' }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker, Git and Trivy installions') {
            steps {
                sh 'docker -v'
                sh 'trivy -v'
            }
        }
        stage('Build docker image') {
            steps {
                sh 'docker image build -t szgyuval123/mission-repo:$GIT_COMMIT .'
            }
        }

        stage('Trivy Vulnerability Scanner') {
            steps {
                sh '''
                    trivy image --scanners vuln --severity HIGH,CRITICAL --format json --output trivy-image-CRITICAL-HIGH-results.json szgyuval123/mission-repo:$GIT_COMMIT
                '''
            }
            post {
                always {
                    sh '''
                        trivy convert \
                            --format template --template "@/usr/local/share/trivy/templates/html.tpl" \
                            --output trivy-image-CRITICAL-HIGH-results.html trivy-image-CRITICAL-HIGH-results.json
                        trivy convert \
                            --format template --template "@/usr/local/share/trivy/templates/junit.tpl" \
                            --output trivy-image-CRITICAL-HIGH-results.xml trivy-image-CRITICAL-HIGH-results.json
                    '''
                }
            }
        }

        stage('Pushing Image to docker repository') {
            steps {
                withDockerRegistry(credentialsId: 'docker-hub-creds', url: "") {
                    sh 'docker image push szgyuval123/mission-repo:$GIT_COMMIT'
                }
            }
        }

        stage('Installing helm component on k8s cluster') {
            steps {
                sh 'curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash'
                sh 'helm version'
            }
        }

        stage('Adding ingress nginx helm repo') {
            steps {
                sh 'helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx'
                sh 'helm repo update'
            }
        }

        stage('Installing ingress controller') {
            steps {
                sh '''
                    if ! helm status ingress-nginx -n ingress-nginx > /dev/null 2>&1; then
                        echo "Ingress-Nginx not found. Installing..."
                        helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=NodePort
                    else
                        echo "Ingress-Nginx already installed. Skipping installation."
                    fi
                '''
            }
        }

        stage('Creating Helm Chart for Web Application') {
            steps {
                sh '''
                    if [ ! -d "web-app-chart" ]; then
                        echo "Directory does not exist. Creating Helm chart"
                        helm create web-app-chart
                    fi
                    echo "replacing default .yaml files with app files"
                    rm -f web-app-chart/templates/*.yaml
                    mv web-app-deployment.yaml web-app-chart/templates/
                    mv web-app-service.yaml web-app-chart/templates/
                    mv web-app-namespace.yaml web-app-chart/templates/
                    mv web-app-ingress.yaml web-app-chart/templates/
                '''
            }
        }

        stage('Deploying Helm Chart') {
            steps {
                sh '''
                    helm upgrade --install web-app ./web-app-chart \
                    -f values.yaml \
                    --set image.tag=$GIT_COMMIT
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, skipMarkingBuildUnstable: true, testResults: 'trivy-image-CRITICAL-HIGH-results.xml'

            publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, icon: '', keepAll: true, reportDir: './',
             reportFiles: 'trivy-image-CRITICAL-HIGH-results.html', reportName: 'Trivy Image Critical-High Vulnerabilities Report',
             reportTitles: '', useWrapperFileDirectly: true])

            emailext body: '''Build finished with status: ${currentBuild.currentResult}
            Job: ${env.JOB_NAME}
            Build number: ${env.BUILD_NUMBER}
            URL: ${env.BUILD_URL}''', subject: 'Jenkins Build - ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}',
            to: 'yuval100r@gmail.com'
            mimeType: 'text/plain'
        }
    }
}