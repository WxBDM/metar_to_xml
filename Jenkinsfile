#!/usr/bin/env groovy

pipeline {
    agent {
        any { image 'python:3' }
    }
    stages {
        stage('build') {
            steps {
              sh "source mtx/bin/activate && python3 -m pip freeze"
            }
        }
        stage("Unittest") {
            steps {
                echo '=== This is the unittest stage. ==='
                sh 'python3 tests/test_utils.py'
                echo 'Unit testing finished.'
            }
        }
        stage("PyTest") {
            steps {
                echo '===This is the pytest stage. ==='
                echo 'PyTest testing finished.'
            }
        }
        stage("METAR Test") {
            steps {
                echo '=== This is the metar test stage. ==='
                echo 'METAR testing finished.'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'build/libs/**/*.jar', fingerprint: true
        }
    }
}
