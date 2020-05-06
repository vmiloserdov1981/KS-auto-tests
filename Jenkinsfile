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
    parameters {
      string defaultValue: 'http://10.10.20.39:4444/wd/hub', description: 'переменная с адресом селеноида', name: 'SELENOID_IP', trim: false
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
                sh 'pytest --alluredir=reports/'
            }
            steps {
                allure jdk: '', results: [[path: "reports/"]]
            }
        }
    }
    post{
      always {
        cleanup{
            cleanWs()
        }
    }
}