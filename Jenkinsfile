#!/usr/bin/env groovy

pipeline {
    agent { docker { image 'python:3.8.3' } }

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
            always {
                
            }
        }
        stage("METAR Test") {
            steps {
                echo "This is the metar test stage."
            }
        }
	post {
		always {
			junit '**/target/reports/test-*.xml'
		}
	}
    }
}

