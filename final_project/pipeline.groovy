properties([disableConcurrentBuilds()])

pipeline {
    agent {
        node {
            label 'master'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
        timestamps()
    }

    stages {

         stage("Preparing") {
            steps {
                echo "one"
                sh "cd $WORKSPACE/final_project && pip install -r requirements.txt"
            }
            }

        stage("Building...") {
            steps {
                echo "two"
                sh "cd $WORKSPACE/final_project && docker-compose up -d"
            }
        }
    }

    post {
        always {
            allure([
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'alluredir']]
            ])
            cleanWs()
        }
    }
}