#!/usr/bin/env groovy

pipeline {
    agent {
        any { image 'python:3' }
    }
    stages {
        stage('Build') {
            steps {
              sh "source mtx/bin/activate && python3 -m pip install -r requirements.txt"
            }
        }
        stage("Testing") {
          steps {
            sh "source mtx/bin/activate && python3 -m py.test"
          }
        }
    }
}
