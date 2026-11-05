// Jenkinsfile - the list of steps Jenkins (the robot helper) runs, in order.
// Cloud logins are NEVER written in this file. In a real run, the owner
// adds them in Jenkins itself with these credential IDs:
//   aws-creds, azure-creds, gcp-creds
// and a stage uses them through withCredentials, for example:
//   withCredentials([string(credentialsId: 'aws-creds', variable: 'AWS_CREDS')]) { ... }
// In dry-run mode (the default here) the deploy scripts never use them.
pipeline {
    agent any

    environment {
        DRY_RUN = 'true'
        VERSION = '1.0.0'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Getting the latest code...'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Installing what the app and tests need...'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests. If a test fails, the pipeline stops here and nothing is deployed.'
                sh 'PYTHONPATH=. python -m pytest -q'
            }
        }
        stage('Package') {
            steps {
                echo 'Packing the app into one artifact file...'
                sh '''mkdir -p artifacts
echo "$VERSION" > artifacts/version.txt
tar -czf artifacts/shop-app.tar.gz app Jenkinsfile
ls -lh artifacts'''
            }
        }
        stage('Deploy to AWS') {
            steps {
                sh 'DRY_RUN=$DRY_RUN bash scripts/deploy_aws.sh'
            }
        }
        stage('Deploy to Azure') {
            steps {
                sh 'DRY_RUN=$DRY_RUN bash scripts/deploy_azure.sh'
            }
        }
        stage('Deploy to GCP') {
            steps {
                sh 'DRY_RUN=$DRY_RUN bash scripts/deploy_gcp.sh'
            }
        }
    }

    post {
        success {
            echo 'All steps finished. The same version was checked for all 3 clouds.'
        }
        failure {
            echo 'Something failed. Fix it and run the job again - Jenkins restarts from the top, and the duplicate guard stops the same version being deployed twice.'
        }
        always {
            archiveArtifacts artifacts: 'artifacts/*', allowEmptyArchive: true
        }
    }
}
