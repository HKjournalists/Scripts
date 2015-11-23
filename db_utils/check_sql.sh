status=`service mysql status | grep -c running`
if [ $status -eq 0 ] ; then
   service mysql start 
fi
