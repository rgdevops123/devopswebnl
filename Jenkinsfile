node {
    def app

    stage('Clone repository') {
        /* Clone the repository to our workspace */

        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("rgdevops123/devopswebnl")
    }

    stage('Test image') {
        /* Run a test framework against our image. */

        app.inside {
            sh 'pytest -v --disable-pytest-warnings'
        }
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag. */
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}
