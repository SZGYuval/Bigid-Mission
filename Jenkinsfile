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
    agent {
        label 'Jenkins-Agent'   // must match your EC2 cloud template label
    }

    stages {
        stage('Run on EC2') {
            steps {
                sh 'echo Hello from EC2 agent!'
            }
        }
    }
}