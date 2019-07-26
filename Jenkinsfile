pipeline{
    agent any
     // environment {
        
    //      FLASK_APP='hello_flask.py'
    //      FLASK_ENV='production'
    //   }
     //  tools {nodejs "nodejs"}
    //   triggers {
    //     pollSCM('* * * * *')
    // }
    
    stages{
        stage('checkout'){
            steps{
                 //withCredentials([string(credentialsId: 'prgit', variable: 'git')]) {
                 //echo "My password is '${git}'!"
                 checkout([$class: 'GitSCM',
                 branches: [[name: 'origin/master']],
                 extensions: [[$class: 'WipeWorkspace']],
                 userRemoteConfigs: [[url: 'https://github.com/Nimisha-97/Weather-app.git']]
                ])
            }
        }
       
    //  stage ('dependencies'){
    //         steps{
    //         sh 'cd weather;pip install -r requirements.txt;'
    //         sh 'cd weather;npm install;'
    //              }
    //     }
            stage ('zip'){
               steps
               {
                 sh 'zip -r weather.zip ./weather'
            }
        }
       stage ( 'nexus')
        {
            steps{
                withCredentials([usernamePassword(credentialsId: 'sudipa_nexus', passwordVariable: 'pass', usernameVariable: 'usr')]){
                sh 'curl -u ${usr}:${pass} --upload-file weather.zip http://3.17.164.37:8081/nexus/content/repositories/devopstraining/Nimisha-python/weather-${BUILD_NUMBER}.zip'
            }
            }
        }
        stage ('Deploy') {
            steps {
               withCredentials([file(credentialsId: 'deployment-server', variable: 'secret_key_for_tomcat')]) {
                  sh 'scp -i ${secret_key_for_tomcat} weather.zip ubuntu@18.224.182.74:~/'
                  sh 'ssh -i ${secret_key_for_tomcat} ubuntu@18.224.182.74 "cd ~;unzip weather.zip -d ./weather;"'
                  sh 'ssh -i ${secret_key_for_tomcat} ubuntu@18.224.182.74 "cd ~;cd weather;cd weather;pm2 start "python api.py";"'
               }
            }
        }
 }
    post {
        success {
             slackSend (color: '#00FF00', message: " SUCCESSFUL: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
         }
         failure {
             slackSend (color: '#FF0000', message: " FAILED: Job '${JOB_NAME} [${BUILD_NUMBER}]' (${BUILD_URL})")
         }
    }
 }