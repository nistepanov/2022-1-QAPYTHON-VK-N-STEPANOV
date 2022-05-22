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
        stage("Building...") {
            steps {
                echo "two"
                sh "cd $WORKSPACE/final_project && /usr/local/bin/docker-compose up -d"
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