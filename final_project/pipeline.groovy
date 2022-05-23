properties([disableConcurrentBuilds()])

pipeline {
        environment {
        PATH = "$PATH:/usr/local/bin"
    }
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

         stage("Building...") {
            steps {
                echo "two"
                sh "cd $WORKSPACE/final_project && docker-compose up -d"
            }
        }

        stage("Dropping containers...") {
            steps {
                echo "two"
                sh "cd $WORKSPACE/final_project docker wait tests_qa"
                sh "cd $WORKSPACE/final_project && docker-compose down -v"
            }
        }
    }

    post {
        always {
            allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-report']]
            ])
            cleanWs()
        }
    }
}