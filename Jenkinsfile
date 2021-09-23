#!/usr/bin/env groovy

pipeline {
    agent {
        any { image 'python:3' }
    }
    stages {
        stage('Install Packages') {
            steps {
              sh "source mtx/bin/activate && python ${env.WORKSPACE}/tests/pytest-dependency-0.5.1/setup.py install && rm -r ${env.WORKSPACE}/tests/pytest-dependency-0.5.1"
              sh "source mtx/bin/activate && python3 -m pip install -r requirements.txt"
              sh "source mtx/bin/activate && python3 -m pip freeze"
            }
        }
        stage("Testing Utils") {
          steps {
            sh "source mtx/bin/activate && pytest ${env.WORKSPACE}/tests/test_utils.py"
          }
        }
        stage("Testing Parser") {
          steps {
            sh "source mtx/bin/activate && pytest ${env.WORKSPACE}/tests/test_parser.py"
          }
        }
    }
}
