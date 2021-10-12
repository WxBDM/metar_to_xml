#!/usr/bin/env groovy

pipeline {
    agent {
        any { image 'python:3' }
    }
    stages {
        stage('Install Packages') {
            steps {
              sh "source mtx/bin/activate && python3 -m pip install -r requirements.txt"
            }
        }
        stage("Testing Utils") {
          steps {
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
              sh "source mtx/bin/activate && pytest ${env.WORKSPACE}/tests/test_utils.py --verbose"
            }
          }
        }
        stage("Testing Parser") {
          steps {
              catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh "source mtx/bin/activate && pytest ${env.WORKSPACE}/tests/test_parser.py --verbose"
              }
          }
        }
        stage("Testing Formatter") {
          steps {
              catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh "source mtx/bin/activate && pytest ${env.WORKSPACE}/tests/test_formatter.py --verbose"
              }
          }
        }
    }
    post {
      always {
        cleanWs()
      }
    }
}
