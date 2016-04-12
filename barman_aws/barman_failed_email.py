import boto
import boto.s3
import sys
from boto.s3.key import Key
import subprocess as sub
#!/usr/bin/python

import smtplib
import datetime
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
import email
import os

def mail_send():
    now = datetime.datetime.now()
    sender = 'nirbhayk@leotechnosoft.net'
    receivers = ['nirbhay@ajency.in']
    #receivers = ['nirbhayk@leotechnosoft.net','vivekj@leotechnosoft.net']
    #receivers = ['nirbhayk@leotechnosoft.net',]
    msg = MIMEMultipart()
    msg['Subject'] = 'Barman Status Check failed'
    #msg['From'] = 'nirbhayk@leotechnosoft.net'
    msg['From'] = 'no-reply@ajency.in'
    msg['To'] = 'birbhay@aj.com'
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
    smtpObj = smtplib.SMTP('smtp.1and1.com')
    smtpObj.login("nirbhayk@leotechnosoft.net", "nirbhay@327")
    smtpObj.sendmail(sender, receivers, msg.as_string())

mail_send()
