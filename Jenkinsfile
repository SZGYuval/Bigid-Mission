pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Print environment varaible') {
            steps {
                sh 'printenv'
            }
        }
    }
}