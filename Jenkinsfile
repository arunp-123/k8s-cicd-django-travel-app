pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        DOCKER_IMAGE = "arun1278/django-backend"
        DOCKER_TAG = "v1"
        KUBECONFIG_CRED = "kubeconfig-jenkins"
        GIT_CRED = "git"              // ✅ Correct Git credential ID
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
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CRED}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                        # Create Docker config.json for Kaniko
                        mkdir -p /kaniko/.docker
                        echo "{\"auths\":{\"https://index.docker.io/v1/\":{\"username\":\"$DOCKER_USER\",\"password\":\"$DOCKER_PASS\"}}}" > /kaniko/.docker/config.json

                        # Run Kaniko to build & push image
                        kubectl run kaniko --rm -i --restart=Never --image=gcr.io/kaniko-project/executor:latest --namespace=jenkins -- \
                          --dockerfile=Dockerfile \
                          --context=git://github.com/arunp-123/django-travel-application.git \
                          --destination=docker.io/arun1278/django-backend:v1
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
