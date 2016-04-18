#echo "++++++RUNIING HEALTH CHECK" >> /tmp/barman_run.log
cnt=`barman check main | grep -v "WARNING" | grep -c "FAILED"`
if [ $cnt -ne 0 ] ; then
    echo "FAILED"
    python /home/ubuntu/scripts/barman_failed_email.py
else
   echo "OK"
   python /home/ubuntu/scripts/barman_failed_email.py
fi

