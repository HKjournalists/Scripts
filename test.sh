if [ `ps aux | grep -v 'grep' | grep -c mysql` -eq 0 ] ; then
   echo "stopped"
else
   echo "running"
fi
