pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }
  }
  stages {
    stage('build') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh "pytest --alluredir=reports"
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