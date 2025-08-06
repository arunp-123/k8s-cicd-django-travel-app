pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        DOCKER_IMAGE = "arun1278/django-backend"
        DOCKER_TAG = "v1"
        KUBECONFIG_CRED = "kubeconfig-jenkins"
        GIT_CRED = "git"
        DOCKERHUB_CRED = "dockerhub-cred"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master',
                    credentialsId: "${GIT_CRED}",
                    url: 'https://github.com/arunp-123/django-travel-application.git'
            }
        }

        stage('Build & Push Image with Kaniko') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CRED}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                        sh '''
                            set -e
                            export KUBECONFIG=$KUBECONFIG_FILE

                            echo "🔑 Creating DockerHub secret..."
                            kubectl delete secret regcred --ignore-not-found -n jenkins
                            kubectl create secret docker-registry regcred \
                              --docker-server=https://index.docker.io/v1/ \
                              --docker-username=$DOCKER_USER \
                              --docker-password=$DOCKER_PASS \
                              -n jenkins

                            echo "🚀 Running Kaniko build pod..."
                            kubectl apply -f k8s/kaniko-job.yaml -n jenkins

                            echo "⏳ Waiting for Kaniko build to finish..."
                            kubectl wait --for=condition=complete job/kaniko-build -n jenkins --timeout=300s
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        kubectl apply -f k8s/django-travel-application.yml -n jenkins
                        kubectl rollout status deployment/django-application -n jenkins
                    '''
                }
            }
        }
    }
}
