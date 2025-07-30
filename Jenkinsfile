// pipeline {
//     agent any
//
//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }
//         stage('Print environment varaible') {
//             steps {
//                 sh 'printenv'
//             }
//         }
//     }
// }

pipeline {
    agent { label 'aws-ec2-instance-docker' }
    stages {
        stage('Test') {
            steps {
                sh 'echo Hello from EC2 agent'
            }
        }
    }
}
