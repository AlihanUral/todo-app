pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'alihanural'
        BACKEND_IMAGE = 'alihanural/todo-backend:latest'
        FRONTEND_IMAGE = 'alihanural/todo-frontend:latest'
    }

    stages {

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                    docker build \
                        -t $BACKEND_IMAGE \
                        ./backend
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                    docker build \
                        -t $FRONTEND_IMAGE \
                        ./frontend
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                    docker push $BACKEND_IMAGE
                    docker push $FRONTEND_IMAGE
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}
