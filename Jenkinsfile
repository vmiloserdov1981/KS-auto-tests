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
                sh 'python get-pip.py pip==19.3.1'
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