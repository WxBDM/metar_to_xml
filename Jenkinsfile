#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Beginning build step'
                virtualenv venv --distribute
                . venv/bin/activate
                sh 'pip install -r requirements.txt'
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
