import boto
import boto.s3
import sys
from boto.s3.key import Key
import subprocess as sub

import smtplib
import datetime
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
import email
import os

from email_config import sender,receivers,EMAIL_HOST,USERNAME,PASSWORD

def mail_send():
    now = datetime.datetime.now()
    msg = MIMEMultipart()
    msg['Subject'] = 'Barman Status Check failed'
    msg['From'] = 'nirbhay@ajency.in'
    msg['To'] = 'backupnotify@ajency.in'
#    msg['Cc'] = 'abhisheks@leotechnosoft.net, nirbhayk@leotechnosoft.net'
    p = sub.Popen(['barman', "check", "main" ],stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()
    txt = """Hi , 
    
Something went wrong with barman.Please check\n%s\n
    
-- 
    """ %(output,)
    cur_date = "%d" %now.day
    cur_month = "%d" %now.month
    cur_year = "%d" %now.year
    txt = txt.format(str(cur_date + " " + now.strftime('%B') + " " + cur_year ))
    msg.attach(email.mime.Text.MIMEText(txt))  
    smtpObj = smtplib.SMTP(EMAIL_HOST)
    smtpObj.starttls()
    smtpObj.login(USERNAME, PASSWORD)
    smtpObj.sendmail(sender, receivers, msg.as_string())
    smtpObj.quit()

mail_send()
