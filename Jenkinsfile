pipeline {
    agent any

    environment {
        IMAGE_NAME = "riethuram/cicd-app"
    }

    stages {

        stage('Build Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Push Image') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        docker.image("${IMAGE_NAME}").push("latest")
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                docker stop cicd-container || exit 0
                docker rm cicd-container || exit 0
                docker run -d -p 5000:5000 --name cicd-container %IMAGE_NAME%
                '''
            }
        }
    }
}
