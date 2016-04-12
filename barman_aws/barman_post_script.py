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
from AWS_ACCESS import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY 

def mail_send(url):
    now = datetime.datetime.now()
    sender = 'nirbhayk@leotechnosoft.net'
    receivers = ['nirbhay@ajency.in']
    msg = MIMEMultipart()
    msg['Subject'] = 'Barman Status Email'
    msg['From'] = 'no-reply@ajency.in'
    msg['To'] = 'receivers@ajency.in'
    p = sub.Popen(['barman', "list-backup", "main" ],stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()
    txt = """Hi , 
URL will get exire in 7 days
Backup download URl\n%s \n\n
BARMAN status content.\n\n\n%s\n
    
-- 

    """ %(url,output,)
    cur_date = "%d" %now.day
    cur_month = "%d" %now.month
    cur_year = "%d" %now.year
    txt = txt.format(str(cur_date + " " + now.strftime('%B') + " " + cur_year ))
    msg.attach(email.mime.Text.MIMEText(txt))  
    smtpObj = smtplib.SMTP('smtp.1and1.com')
    smtpObj.login("nirbhayk@leotechnosoft.net", "nirbhay@327")
    smtpObj.sendmail(sender, receivers, msg.as_string())

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


BARMAN_SOURCE = '/var/lib/barman/main/'
GZIP_LOCATION = '/tmp/testgzip.tar.gz'

bucket_name = "barmandump"
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)


bucket = conn.create_bucket(bucket_name,
    location=boto.s3.connection.Location.DEFAULT)

testfile = GZIP_LOCATION

ZIP_COMMAND = "tar -zcvf {} {}".format(GZIP_LOCATION,BARMAN_SOURCE)
#p = os.system(ZIP_COMMAND)

print 'Uploading %s to Amazon S3 bucket %s' % \
   (testfile, bucket_name)
k = Key(bucket)
k.key = 'mainzipfile.gz'
k.set_contents_from_filename(testfile,
    cb=percent_cb, num_cb=1)
k.set_acl('public-read')
url = k.generate_url(expires_in=3600*24*7)
mail_send(url)

