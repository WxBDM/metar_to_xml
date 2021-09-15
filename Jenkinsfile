#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Beginning build step'
                git branch: 'main', url: 'https://github.com/WxBDM/metar_to_xml'
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
