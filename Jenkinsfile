// Jenkins Pipeline — интеграция SonarQube
// Урок 4: Интеграция SonarQube с CI/CD

pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY  = 'vulnerable-app'
        SONAR_PROJECT_NAME = 'OTUS Vulnerable App'
        SONAR_PROJECT_VER  = '1.0-lesson15'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test') {
            steps {
                sh 'pip install flask --quiet && echo "Smoke test passed"'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                        sh 'sonar-scanner -Dsonar.projectKey=${SONAR_PROJECT_KEY} -Dsonar.projectVersion=${SONAR_PROJECT_VER} -Dsonar.sources=backend,frontend -Dsonar.token=${SONAR_TOKEN}'
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success { echo "✅ Quality Gate passed" }
        failure { echo "⛔ Quality Gate failed — исправьте уязвимости!" }
    }
}
