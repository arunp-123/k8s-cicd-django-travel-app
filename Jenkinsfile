pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'arun1278/django-backend'
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG_CRED = "kubeconfig-jenkins"
        GIT_CRED = "git"
        DOCKERHUB_CRED = "dockerhub-cred"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    credentialsId: "${GIT_CRED}",
                    url: 'https://github.com/arunp-123/django-travel-application.git'
            }
        }

        stage('Install Python Dependencies & Run Tests') {
            steps {
                script {
                    echo '📦 Installing dependencies and running tests...'
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        # Run Django tests
                        python manage.py test || true
                    '''
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CRED}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        echo "🐳 Building & pushing Docker image..."
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG .
                            docker push $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                            docker tag $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG $DOCKER_REGISTRY/$IMAGE_NAME:latest
                            docker push $DOCKER_REGISTRY/$IMAGE_NAME:latest
                        '''
                    }
                }
            }
        }

        stage('Verify Kubernetes Connectivity') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        echo '🔍 Checking Kubernetes cluster info...'
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
                        echo '🚀 Updating image in Kubernetes manifests...'
                        sed -i "s|image: .*|image: $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG|g" k8s/django-travel-application.yml
                        
                        echo '📦 Applying Kubernetes manifests...'
                        kubectl apply -f k8s/django-travel-application.yml -n jenkins

                        echo '⏳ Waiting for rollout to complete...'
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
                        echo '🔍 Verifying pods and services...'
                        kubectl get pods -n jenkins -o wide
                        kubectl get svc -n jenkins
                        kubectl wait --for=condition=ready pod -l app=django-app -n jenkins --timeout=300s
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
