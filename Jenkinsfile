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
                    image 'python:rc-buster'
                    args "-v ${PWD}:/app -w /app"
                    reuseNode true
                    label "GazBank_test"
                }
            }
            steps {
                sh 'python --version'
                sh 'pip3 --version'
                sh 'pip install -U "pip<20" -r requirements.txt'
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