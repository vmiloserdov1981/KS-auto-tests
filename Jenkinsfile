pipeline {
  agent { 
    docker { 
    image 'python:3.7.7' 
    } 
  }
  stages {
    stage('build') {
      steps {
        sh 'sudo -H pip install -r requirements.txt'
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