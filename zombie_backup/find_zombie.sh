cnt=`ps -aux | tr -s " " | cut -d " " -f8 | grep -ic "r"`
if [ $cnt -gt 0 ] ; then
    sshpass -pleo_123 ssh vinayk@172.16.0.145 -p 22  'ps -aux | tr -s " " | cut -d " " -f2,11' > zombie_report.txt
    python /home/phaniv/nirbhay/scripts/zombie/mail.py
 #   mail -s "Backup Status" nirbhayk@leotechnosoft.net < $HOME/zombie_report.txt
fi    
