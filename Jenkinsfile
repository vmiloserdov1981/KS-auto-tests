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
                dockerfile {
                    filename "Dockerfile"
                }
            }
            steps {
//                sh "service docker start"
//                sh "curl -s https://aerokube.com/cm/bash | sh"
//                sh "./cm selenoid start --browsers 'chrome:80.0'"
                sh 'pytest --alluredir=reports'
            }
        }
    }
    post{
      always {
        allure includeProperties: false, jdk: '', results: [[path: 'reports']]
        }
      cleanup{
            cleanWs()
        }
    }
}