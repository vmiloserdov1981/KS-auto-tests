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
        stage("Prepare build image") {
            steps {
                sh "docker build -f Dockerfile . -t gazbank:test"
            }
        }
        stage("Build project") {
            agent {
                docker {
                    image 'gazbank:test'
                    args "-v ${PWD}:/app -w /app"
                    reuseNode true
                    label "gazbank_test"
                }
            }
            steps {
                sh 'pip3 freeze'
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