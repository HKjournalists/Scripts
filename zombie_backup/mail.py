#!/usr/bin/python
import smtplib
import csv
import xlrd
import datetime
import MySQLdb
import email
from email.mime.multipart import MIMEMultipart
import twilio
import twilio.rest
import datetime
from time import gmtime, strftime , localtime


# Open database connection

# prepare a cursor object using cursor() method

# execute SQL query using execute() method.
# query = "select * from hesk_tickets limit 1 ;"
class no_record_error(Exception):
    pass

def send_mail():
    now = datetime.datetime.now()
    path = "zombie_report.txt"
    file = open(path, 'r')
    html = ""
    for line in file:
        html = html + str(line)
    sender = 'nirbhayk@leotechnosoft.net'
    # receivers = ['nirbhayk@leotechnosoft.net','abhisheks@leotechnosoft.net','vivekj@leotechnosoft.net']
    receivers = ['nirbhayk@leotechnosoft.net','phaniv@leotechnosoft.net']
#     receivers = ['nirbhayk@leotechnosoft.net',]
    msg = MIMEMultipart()
    now = datetime.datetime.now()
    cur_date = "%d" %now.day
    cur_month = "%d" %now.month
    cur_year = "%d" %now.year
    t = 'Zombie report ({}{})'
    msg['Subject'] = t.format(str(cur_date + " " + now.strftime('%B') + " " + cur_year ),strftime(" %H:%M:%S", localtime()))
    msg['From'] = 'zombie_informer'
    msg['To'] = 'tusharthorat@leotechnosoft.net'
    # msg['Cc'] = 'abhisheks@leotechnosoft.net'
    print html
    msg.attach(email.mime.Text.MIMEText(html))
    smtpObj = smtplib.SMTP('smtp.1and1.com')
    smtpObj.login("nirbhayk@leotechnosoft.net", "nirbhay@327")
    smtpObj.sendmail(sender, receivers, msg.as_string())


now = datetime.datetime.now()
d = now.strftime("%a")
day_text = "Today is " + str(now.strftime("%A"))
print day_text
import subprocess
for x in range(1,5):
    try:
        send_mail()
        print "Mail sent Successfully"
        msg_text = "Daily timesheet mail has been send successfully."
        break
    except no_record_error:
        print "Excel file not found"
        msg_text = "Excel file not found or empty"
        break
    except Exception as ex:
        print "Daily timesheet Mail Sending Failed,\n Retrying ",
        msg_text = "Error occured while sending Daily timsheet mail.Please check immediately"
        print "Error : " + str(ex)
        print ".." * 30


for x in range(1,5):
    try:
        print "Sending SMS to +919762310831"
        account_sid = "AC78f4a614e508e1dcadc3fbfbb80da4aa"
        auth_token = "7aaafbbb589a0a3a5934a4a38563effd"
        client = twilio.rest.TwilioRestClient(account_sid, auth_token)
        msg_text = "Hi Tushar!\n"+msg_text 
        message = client.messages.create(
            body=msg_text,
            to="+919762310831",
            from_="+15014294699"
        )
        print "Message sending completed"
        break
    except Exception as e:
            print "Error occurred while sending message"
            print e
