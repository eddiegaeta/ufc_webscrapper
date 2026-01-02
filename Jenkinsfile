pipeline {
    agent {
        docker {
            image 'edthegreat/jenkins-docker-agent:1.0.0'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DOCKER_API_VERSION = '1.41'
        HELM_RELEASE_NAME = 'ufc-webscrapper'
        HELM_NAMESPACE = 'default'
    }

    stages {
        stage('SCM Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/eddiegaeta/ufc_webscrapper.git'
            }
        }

        stage('Setup Kubeconfig') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'KUBECONFIG', variable: 'KUBECONFIG_FILE')]) {
                        sh '''
                        mkdir -p ~/.kube
                        cp $KUBECONFIG_FILE ~/.kube/config
                        chmod 600 ~/.kube/config
                        kubectl cluster-info
                        '''
                    }
                }
            }
        }

        stage('Helm Lint') {
            steps {
                dir('helm-chart') {
                    sh 'helm lint .'
                }
            }
        }

        stage('Helm Deploy') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'KUBECONFIG', variable: 'KUBECONFIG_FILE')]) {
                        dir('helm-chart') {
                            sh '''
                            export KUBECONFIG=$KUBECONFIG_FILE
                            helm upgrade --install ${HELM_RELEASE_NAME} . \
                                --namespace ${HELM_NAMESPACE} \
                                --create-namespace \
                                --wait \
                                --timeout 5m
                            '''
                        }
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'KUBECONFIG', variable: 'KUBECONFIG_FILE')]) {
                        sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        kubectl get pods -n ${HELM_NAMESPACE}
                        kubectl get services -n ${HELM_NAMESPACE}
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
