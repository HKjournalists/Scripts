cnt=`ps -aux | tr -s " " | cut -d " " -f8 | grep -ic "r"`
echo "Zombie process = " $cnt
if [ $cnt -gt 0 ] ; then
    sshpass -pleo_123 ssh vinayk@172.16.0.145 -p 22  'ps -aux | tr -s " " | cut -d " " -f2,11' > /home/phaniv/Desktop/Tushar_thorat/zombie/zombie_report.txt
    python /home/phaniv/Desktop/Tushar_thorat/zombie/mail.py
fi  
