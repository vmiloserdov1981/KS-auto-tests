pipeline {
    agent {
  dockerfile {
    filename 'Dockerfile'
  }
}
    stages {
        stage('Run Test') {
            steps{
            sh "python --version"
            sh "pytest --version"
            sh "sudo pytest --alluredir=reports"
            }
        }      
        }
    post{
         always {
          archiveArtifacts artifacts: 'reports/**'
        }
//        cleanup{
//            cleanWs()
//        }
    }
}