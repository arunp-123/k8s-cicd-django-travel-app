pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        DOCKER_IMAGE = "arun1278/django-backend"
        DOCKER_TAG = "v1"
        KUBECONFIG_CRED = "kubeconfig-jenkins"
        GIT_CRED = "git"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master',
                    credentialsId: "${GIT_CRED}",
                    url: 'https://github.com/arunp-123/django-travel-application.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
                    """
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_IMAGE:$DOCKER_TAG
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE

                        # Apply Deployment & Service
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml

                        # Verify rollout
                        kubectl rollout status deployment/django-application -n jenkins
                    '''
                }
            }
        }
    }
}




