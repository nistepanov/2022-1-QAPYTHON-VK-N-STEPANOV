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
                sh "cd $WORKSPACE/final_project && docker-compose up"
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