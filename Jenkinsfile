pipeline { 
    options {
        buildDiscarder(
            logRotator(
                artifactDaysToKeepStr: "",
                artifactNumToKeepStr: "",
                daysToKeepStr: "",
                numToKeepStr: "4"
            )
        )
        disableConcurrentBuilds()
    }

    agent any

    stages {
        stage("Build project") {
            agent {
                docker {
                    image 'python:3.7.7-alpine3.11'
                    args "-v ${PWD}:/app -w /app"
                    reuseNode true
                    label "GazBank_test"
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest --alluredir=reports'
            }
        }
    }
    post{
        always {
            archiveArtifacts artifacts: 'reports/**'
        }
        cleanup{
            cleanWs()
        }
    }
}