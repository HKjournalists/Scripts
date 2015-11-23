n=0
until [ $n -ge 3 ]
do
   ps -ef | grep -i xvfb > /tmp/tmp_kill_xvfb_list.txt
   if [ `cat /tmp/tmp_kill_xvfb_list.txt | grep -c wkhtmltopdf` -eq 0 ] ; then
      cat /tmp/tmp_kill_xvfb_list.txt | awk '{print $2}' | xargs kill -9
      break
   fi
   n=`expr $n + 1`
   echo "Sleeping for 15 seconds"
   echo $n
   sleep 15
done
rm -f /tmp/tmp_kill_xvfb_list.txt

