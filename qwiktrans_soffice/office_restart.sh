netstat -nap | grep -i "soffice" | grep -i "SingleOffice" 
if [ $? -ne 0 ] ; then
     echo "Openoffice not running. Trying to restart"
     /etc/init.d/./openoffice.sh stop
     /etc/init.d/./openoffice.sh start
     if [ $? -ne 0 ] ; then
         echo "Failed to restart openoffice"
     fi
fi
