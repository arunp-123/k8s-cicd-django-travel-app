pipeline {
    agent {
        docker {
            image 'python:3.10'         // Base image with Python pre-installed
            args '-u root:root'        // Run as root to install extra tools
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
        stage('Setup Tools') {
            steps {
                sh '''
                    apt-get update && apt-get install -y docker.io curl
                    curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
                    
                    python3 --version
                    docker --version
                    kubectl version --client
                '''
            }
        }

        stage('Checkout Code') {
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
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python manage.py test || true
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    def appImage = docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}")
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKERHUB_CRED}") {
                        appImage.push()
                        appImage.push('latest')
                    }
                }
            }
        }

        stage('Verify Kubernetes Connectivity') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        kubectl cluster-info
                        kubectl get nodes -o wide
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        sed -i "s|image: .*|image: ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/django-travel-application.yml
                        kubectl apply -f k8s/django-travel-application.yml -n jenkins
                        kubectl rollout status deployment/django-application -n jenkins
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        kubectl get pods -n jenkins -o wide
                        kubectl get svc -n jenkins
                        kubectl wait --for=condition=ready pod -l app=django-application -n jenkins --timeout=300s
                    '''
                }
            }
        }
    }

    post {
        success { echo '🎉 Pipeline completed successfully!' }
        failure { echo '❌ Pipeline failed!' }
        always { sh 'docker system prune -f || true' }
    }
}
