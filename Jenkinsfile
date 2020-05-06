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
                sh 'pytest --alluredir=reports/'
            }
        }
        stage('Publish tests results') {
            allure jdk: '', results: [[path: "reports/"]]
        }
    }
    post{
      always {
        cleanup{
            cleanWs()
        }
    }
}