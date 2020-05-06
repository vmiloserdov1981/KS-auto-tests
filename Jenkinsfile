

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
    properties([
        parameters([
            string(name: 'SELENOID_IP', defaultValue: 'http://10.10.20.39:4444/wd/hub', description: 'переменная с адресом селеноида', )
        ])
    ])

    agent any

    stages {
        stage("Build project") {
            agent {
                dockerfile {
                    filename "Dockerfile"
                }
            }
            steps {
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