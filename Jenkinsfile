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
    }

    post {
        always {
            junit allowEmptyResults: true, skipMarkingBuildUnstable: true, testResults: 'trivy-image-CRITICAL-HIGH-results.xml'

            publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, icon: '', keepAll: true, reportDir: './',
             reportFiles: 'trivy-image-CRITICAL-HIGH-results.html', reportName: 'Trivy Image Critical-High Vulnerabilities Report',
             reportTitles: '', useWrapperFileDirectly: true])
        }
    }
}