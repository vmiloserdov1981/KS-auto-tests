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
                    image 'python:3.6-alpine'
                    args "-v ${PWD}:/app -w /app"
                    reuseNode true
                    label "GazBank_test"
                }
            }
            steps {
                sh 'python --version'
                sh 'pip3 --version'
                sh 'apk update'
                sh 'python -m pip install --upgrade pip'
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