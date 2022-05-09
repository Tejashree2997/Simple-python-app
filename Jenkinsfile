pipeline {
	agent any
	    stages {
	        stage('Clone Repository') {
	        /* Cloning the repository to our workspace */
	        steps {
	        checkout scm
	        }
	   }
	   stage('Build Image') {
	        steps {
	        sh 'sudo docker build -t myapp:v1 .'
	        }
	   }
	   stage('Run Image') {
	        steps {
	        sh 'sudo docker run -d -p 5000:5000 --name my-python-app myapp:v1'
	        }
	   }
	   stage('Testing'){
	        steps {
	            echo 'Testing..'
	            }
	   }
    }
}
