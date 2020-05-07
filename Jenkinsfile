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
    parameters {
      string defaultValue: 'http://10.10.20.39:4444/wd/hub', description: 'переменная с адресом селеноида', name: 'SELENOID_IP', trim: false
    }
    stages {
        stage("Build project") {
            agent {
                dockerfile {
                    filename "Dockerfile"
                }
            }
            steps {
                echo "IP ${params.SELENOID_IP}"
                sh 'pytest --alluredir=reports'
            }
            steps {
                allure jdk: '', results: [[path: "reports"]]
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