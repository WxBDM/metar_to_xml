#!/usr/bin/env groovy

pipeline {
    agent {
        any { image 'python:3' }
    }
    stages {
        stage('Build') {
            steps {
                echo '=== Beginning build step ==='
                sh 'python --version'
                echo 'Build step completed.'
            }
        }
        stage("Unittest") {
            steps {
                echo '=== This is the unittest stage. ==='
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
}
