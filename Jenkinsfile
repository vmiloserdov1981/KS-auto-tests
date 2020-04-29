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
                    filename 'Dockerfile'
                }
            }
            steps {
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