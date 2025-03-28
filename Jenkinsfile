pipeline {
  agent any

  environment {
    REPO = "ghcr.io/saharariel/blackjack-web"
  }

  stages {
    stage('Checkout Code') {
      steps {
        checkout scm
      }
    }
    stage('Read Current Version') {
      steps {
        script {
          // Read the current version from the version.txt file
          if (fileExists(VERSION_FILE)) {
             // If the file exists, read the version number
              def version = readFile(VERSION_FILE).trim()
              def versionParts = version.split("\\.")  // Split the version into parts (major.minor.patch)
              def patch = versionParts[2].toInteger() + 1  // Increment the patch version
              env.VERSION = "${versionParts[0]}.${versionParts[1]}.${patch}"  // Increment patch version
              } else {
              // If the file doesn't exist, start with version 1.0.0
              env.VERSION = "1.0.0"
              }
          echo "Current version: ${env.VERSION}"
        }
      }
    }
    stage('Build Docker Image') {
      steps {
        script {
            // Build the Docker image with the new version tag
            env.IMAGE_TAG = "${REPO}:${env.VERSION}"
            sh """
                docker build -t ${IMAGE_TAG} .
             """
        }
      }
    }

    stage('Login to GHCR') {
      steps {
        withCredentials([string(credentialsId: 'github-pat', variable: 'GITHUB_PAT')]) {
	  sh(script: 'echo "$GITHUB_PAT" | docker login ghcr.io -u saharariel --password-stdin')
        }
      }
    }

    stage('Push to GHCR') {
      steps {
        sh "docker push ${IMAGE_TAG}"
      }
    }

    stage('Print Image Info') {
      steps {
        echo "Pushed image: ${IMAGE_TAG}"
      }
    }
  }
}

