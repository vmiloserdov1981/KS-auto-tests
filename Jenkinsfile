pipeline {
    agent {
  dockerfile {
    filename 'Dockerfile'
  }
}
    stages {
        stage('Run Test') {
            steps{
              sh "pytest --alluredir=reports"
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