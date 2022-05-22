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
                echo "one"
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