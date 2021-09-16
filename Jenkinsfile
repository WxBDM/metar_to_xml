#!/usr/bin/env groovy

pipeline {
    agent {
        any { image 'python:3' }
    }
    stages {
        stage('Build') {
            steps {
                echo '=== Beginning build step ==='
                pip install -r requirements.txt
                echo 'Build step completed.'
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
