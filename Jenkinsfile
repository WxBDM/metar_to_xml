#!/usr/bin/env groovy

pipeline {
    agent {
        any { image 'python:3' }
    }
    stages {
        stage('Build') {
            steps {
                echo 'Beginning build step'
                sh './pip.sh'
                echo 'Build step completed.'
            }
        }
        stage("Unittest") {
            steps {
                echo 'This is the unittest stage.'
            }
        }
        stage("PyTest") {
            steps {
                echo 'This is the pytest stage.'
            }
        }
        stage("METAR Test") {
            steps {
                echo "This is the metar test stage."
            }
        }
    }
}
