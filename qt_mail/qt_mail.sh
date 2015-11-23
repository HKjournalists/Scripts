echo -e "\n\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" >> /home/phaniv/nirbhay/log/mail.log
echo `date -R` >> /home/phaniv/nirbhay/log/mail.log
echo "cron job started" >> /home/phaniv/nirbhay/log/mail.log
source "/home/phaniv/nirbhay/virtual_evn/sms/bin/activate"
python /home/phaniv/nirbhay/scripts/qt_mail/views.py >> /home/phaniv/nirbhay/log/mail.log
echo "cron job completed " >> /home/phaniv/nirbhay/log/mail.log
echo `date -R` >> /home/phaniv/nirbhay/log/mail.log
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" >> /home/phaniv/nirbhay/log/mail.log
