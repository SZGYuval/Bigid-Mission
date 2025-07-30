pipeline {
    agent any {label 'aws slave node'}

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