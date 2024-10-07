pipeline {
    agent any

    environment {
        VIRTUALENV = 'venv'
        PIP_REQUIREMENTS = 'requirements.txt'
        DOCKER_IMAGE = 'shreyanshagrawal0/notes-django'  // Replace with your DockerHub repo
        DOCKER_TAG = "${GIT_COMMIT}"  // Use commit hash as the Docker tag
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'  // Jenkins credentials ID for DockerHub
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning private repository...'
                git credentialsId: 'notes-django-github-credentials', 
                    url: 'https://github.com/agrawalshreyansh0/notes-app.git',
                    branch: 'main'  // Ensure the branch is correct
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up virtual environment...'
                sh '''
                    python3 -m venv $VIRTUALENV
                    . $VIRTUALENV/bin/activate
                    pip install -r $PIP_REQUIREMENTS
                '''
            }
        }

        stage('Run Migrations') {
            steps {
                echo 'Applying migrations...'
                sh '''
                    . $VIRTUALENV/bin/activate
                    python manage.py migrate
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    . $VIRTUALENV/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Static Files Collection') {
            steps {
                echo 'Collecting static files...'
                sh '''
                    . $VIRTUALENV/bin/activate
                    python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    def commitHash = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    docker.build("${DOCKER_IMAGE}:${commitHash}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh '''
                            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                            docker push $DOCKER_IMAGE:$DOCKER_TAG
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf $VIRTUALENV'
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
