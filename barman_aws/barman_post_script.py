import boto
import boto.s3
import sys
from boto.s3.key import Key
import subprocess as sub
import tarfile
#!/usr/bin/python
import smtplib
import datetime
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
import email
import os
from AWS_ACCESS import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,BUCKET_NAME
from config import sender,receivers,EMAIL_HOST,USERNAME,PASSWORD,BARMAN_SOURCE,GZIP_LOCATION

def mail_send(url):
    print "mail_send function triggered"
    now = datetime.datetime.now()
    print "Time = ", now
    msg = MIMEMultipart()
    msg['Subject'] = 'Barman Status Email'
    msg['From'] = 'no-reply@ajency.in'
    msg['To'] = 'receivers@ajency.in'
    #print "Barman list backup command triggered"
    #p = sub.Popen(['barman', "list-backup", "main" ],stdout=sub.PIPE,stderr=sub.PIPE)
    #output, errors = p.communicate()
    txt = """Hi , 
URL will get exire in 7 days
Backup download URl\n%s \n\n
-- 

    """ %(url,)
    cur_date = "%d" %now.day
    cur_month = "%d" %now.month
    cur_year = "%d" %now.year
    txt = txt.format(str(cur_date + " " + now.strftime('%B') + " " + cur_year ))
    msg.attach(email.mime.Text.MIMEText(txt))  
    print "Email  message created"
    smtpObj = smtplib.SMTP(EMAIL_HOST)
    smtpObj.starttls()
    print "Performing login to email account"
    smtpObj.login(USERNAME, PASSWORD)
    print "Login Completed"
    print "Triggering Email sending"
    smtpObj.sendmail(sender, receivers, msg.as_string())
    print "Email Sent"

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def run():
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
           AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(BUCKET_NAME,
             location=boto.s3.connection.Location.DEFAULT)

    testfile = GZIP_LOCATION
    make_tarfile(GZIP_LOCATION, BARMAN_SOURCE)

    #ZIP_COMMAND = "tar -zcvf {} {}".format(GZIP_LOCATION,BARMAN_SOURCE)
    #p = os.system(ZIP_COMMAND)

    print '=========Uploading %s to Amazon S3 bucket %s=============' % \
       (testfile, BUCKET_NAME)
    k = Key(bucket)
    k.key = 'mainzipfile.gz'
    k.set_contents_from_filename(testfile,
        cb=percent_cb, num_cb=1)
    print "FILE SENDING COMPLETED"
    k.set_acl('public-read')
    print "Set as public access"
    url = k.generate_url(expires_in=3600*24*7)
    print "=========Mail Sending prcess started==================="
    mail_send(url)
    print "===========Mail Send Completed=========================="

try:
    run()
except Exception as ex:
    print "Exce[tion == ", ex

