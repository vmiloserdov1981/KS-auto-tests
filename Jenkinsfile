def SELENOID_IP

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
                SELENOID_IP = "http://10.10.20.39:4444/wd/hub"
                echo $SELENOID_IP
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