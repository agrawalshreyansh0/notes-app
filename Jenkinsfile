pipeline {
    agent any

    environment {
        VIRTUALENV = 'venv'
        PIP_REQUIREMENTS = 'requirements.txt'
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

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Add your deployment steps here
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
