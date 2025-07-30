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
                sh 'git -v'
                sh 'trivy -v'
            }
        }
        stage('Build docker image') {
            steps {
                sh 'docker image build -t szgyvual123/bigid-repo:$GIT_COMMIT .'
            }
        }

        stage('Trivy Vulnerability Scanner') {
            steps {
                sh '''
                    trivy image --severity HIGH --format json --output High-result.json szgyvual123/bigid-repo:$GIT_COMMIT
                '''
            }
        }
    }
}