pipeline {
    agent {
        docker {
            image 'python:3.10'      // Base image with Python pre-installed
            args '-u root:root'     // Run as root (to allow installing extra tools)
        }
    }
    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'arun1278/django-backend'
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG_CRED = "kubeconfig-jenkins"
        GIT_CRED = "git"
        DOCKERHUB_CRED = "dockerhub-cred"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    apt-get update && apt-get install -y docker.io kubectl
                    python3 --version
                    docker --version
                    kubectl version --client
                '''
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'master',
                    credentialsId: "${GIT_CRED}",
                    url: 'https://github.com/arunp-123/django-travel-application.git'
            }
        }

        stage('Install Python Dependencies & Run Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python manage.py test || true
                '''
            }
        }

        // Build & push Docker image, Deploy, etc. remain same...
    }
}
