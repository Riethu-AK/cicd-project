pipeline {
    agent any

    environment {
        IMAGE_NAME = "riethuram/cicd-app"
    }

    stages {

        stage('Build Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Push Image') {
            steps {
                bat 'docker login -u riethuram -p STUDENT@KEC'
                bat 'docker push %IMAGE_NAME%'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker stop cicd-container || exit 0'
                bat 'docker rm cicd-container || exit 0'
                bat 'docker run -d -p 5000:5000 --name cicd-container %IMAGE_NAME%'
            }
        }
    }
}
