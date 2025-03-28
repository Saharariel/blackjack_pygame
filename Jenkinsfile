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

    stage('Build Docker Image') {
      steps {
        script {
          def commit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          env.IMAGE_TAG = "${REPO}:${commit}"

          sh """
            docker build -t ${IMAGE_TAG} .
          """
        }
      }
    }

    stage('Login to GHCR') {
      steps {
        withCredentials([string(credentialsId: 'github-pat', variable: 'GITHUB_PAT')]) {
          sh """
            echo "$GITHUB_PAT" | docker login ghcr.io -u saharariel --password-stdin
          """
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

