pipeline {
    agent { label 'aws-slave-node' }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Docker and Git installions') {
            steps {
                sh 'docker -v'
                sh 'git -v'
            }
        }
    }
}