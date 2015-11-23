ps -eo user,pid,etime,cmd | grep soffice.bin | grep -v "grep" > /tmp/temp_soffice.txt
soffice_pids=`cat /tmp/temp_soffice.txt | tr -s " " | cut -d" " -f2 | tr "\n" " "`
if [ -s /tmp/temp_soffice.txt ] ; then
    for id in $soffice_pids
    do
           cnt=`cat /tmp/temp_soffice.txt | grep "$id" | tr -s " " | cut -d " " -f3 | grep -c ":"`
           if [ $cnt -eq 1 ] ; then
                mins=`cat /tmp/temp_soffice.txt | grep "$id" | tr -s " " | cut -d " " -f3 | cut -d":" -f1`
                if [ $mins -lt 5 ] ;then
                   echo "Soffice instance found with less than 5 mins elapsed time with pid="$id
                   echo "Exiting ..."
                   exit
                   echo "kill -9 $id"
                fi
           fi
           echo "\n\nJust output"
           cat /tmp/temp_soffice.txt | grep "$id" 
    done
    echo "killall soffice.bin"
    killall soffice.bin
    /etc/init.d/./openoffice.sh stop
    /etc/init.d/./openoffice.sh start
    
fi
