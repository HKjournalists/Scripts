if [ $# -ne 1 ] 
then
  echo "Please enter version no like 1.0"
else
  cd /home/ubuntu/wikireviews/tags/
  rm -f /tmp/custum_deploy_error
  touch /tmp/custum_deploy_error
   echo "Checkout form SVN for tag-"$1
   svn co http://14.140.226.237/wikireviews/tags/tag-$1/
   if [ $? -ne 0 ]
   then
       echo "Error occurred while svn checkout" >> /tmp/custum_deploy_error
   fi
   echo "Copying bower components from trunc code"
   cp -r /home/ubuntu/wikireviews/trunk/app/bower_components/ /home/ubuntu/wikireviews/tags/tag-$1/app
   if [ $? -ne 0 ]
   then
       echo "Error occurred while copying bower_components" >> /tmp/custum_deploy_error
   fi
   echo "Running JS_merge.sh"
   cd `echo "/home/ubuntu/wikireviews/tags/tag-"$1`
   sh `echo "/home/ubuntu/wikireviews/tags/tag-"$1"/js_merge.sh"`
   if [ $? -ne 0 ]
   then
       echo "Error occurred while running js_merge.sh" >> /tmp/custum_deploy_error
   fi
   echo "Running collectstatic"
   python /home/ubuntu/wikireviews/tags/tag-$1/manage.py collectstatic --noinput
   if [ $? -ne 0 ]
   then
       echo "Error occurred while running collectstatic" >> /tmp/custum_deploy_error
   fi
  echo "Clearing Redis"
  echo "flushall" > /tmp/cust_rdis
  echo "exit" >> /tmp/cust_rdis
  redis-cli < /tmp/cust_rdis
  if [ $? -ne 0 ]
  then
      echo "Error occurred clearing redis" >> /tmp/custum_deploy_error
  fi
  sudo chmod 777 -R `echo "/home/ubuntu/wikireviews/tags/tag-"$1`
  cd ./database_scripts
  if [ $? -ne 0 ]
   then
       echo "Unable to switch to database_scripts" >> /tmp/custum_deploy_error
   fi
  dos2unix implement.sh
  if [ $? -ne 0 ]
   then
       echo "Error in dos2unix " >> /tmp/custum_deploy_error
   fi
  sh implement.sh 
  if [ $? -ne 0 ]
   then
       echo "Error in implement.sh " >> /tmp/custum_deploy_error
   fi
   if [ -s /tmp/custum_deploy_error ]
  then
      cat /tmp/custum_deploy_error
  else
     echo "All steps completed successfully."
     echo "Please change tag version in envvars under /etc/apache/"
  fi


fi
