#!/usr/bin/python

import smtplib
import datetime
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
import twilio
import twilio.rest
import email
import os

def mail_send():
    now = datetime.datetime.now()
    fileMsg = email.mime.base.MIMEBase('application','vnd.ms-excel')
    sender = 'nirbhayk@leotechnosoft.net'
    receivers = ['nirbhayk@leotechnosoft.net','abhisheks@leotechnosoft.net','vivekj@leotechnosoft.net','james@trans-asia.co.jp']
    #receivers = ['nirbhayk@leotechnosoft.net','vivekj@leotechnosoft.net']
    #receivers = ['nirbhayk@leotechnosoft.net',]
    msg = MIMEMultipart()
    msg['Subject'] = 'QwikTrans Daily timesheet'
    #msg['From'] = 'nirbhayk@leotechnosoft.net'
    msg['From'] = 'vivekj@leotechnosoft.net'
    msg['To'] = 'james@trans-asia.co.jp'
    msg['Cc'] = 'abhisheks@leotechnosoft.net, nirbhayk@leotechnosoft.net'
    txt = """Hi James, 
    
Attached is daily time sheet.
    
-- 
Kind Regards,
Vivek Joshi
    """
    cur_date = "%d" %now.day
    cur_month = "%d" %now.month
    cur_year = "%d" %now.year
    fl_name = str(cur_date) + "_" + now.strftime('%b') + "_" + cur_year + "_" + "Tasksheet.xls"
    path = "/home/phaniv/Desktop/QT_Timesheet/" + cur_year + "/" + now.strftime('%B') + "/" + fl_name
    if not os.path.exists("/home/phaniv/Desktop/QT_Timesheet/" + cur_year + "/" + now.strftime('%B') + "/"):
        os.mkdir("/home/phaniv/Desktop/QT_Timesheet/" + cur_year + "/" + now.strftime('%B') + "/")
    txt = txt.format(str(cur_date + " " + now.strftime('%B') + " " + cur_year ))
    msg.attach(email.mime.Text.MIMEText(txt))  
    smtpObj = smtplib.SMTP('smtp.1and1.com')
    smtpObj.login("nirbhayk@leotechnosoft.net", "nirbhay@327")
    fileMsg.set_payload(file(path).read())
    email.encoders.encode_base64(fileMsg)
    fileMsg.add_header('Content-Disposition','attachment;filename='+fl_name)
    msg.attach(fileMsg)
    smtpObj.sendmail(sender, receivers, msg.as_string())
    
        
now = datetime.datetime.now()
d = now.strftime("%a")
day_text = "Today is " + str(now.strftime("%A"))
print day_text
if d.upper() in ['SAT','SUN']:
    print "No need to send mail"
    msg_text = day_text + ".\nNo need to send QT mail"
else:
    for x in range(1,4):
        try:
            mail_send()
            msg_text = "QT mail has been successfully sent to Vivek and Abhishek"
            print "Mail Sent Suceesfully"
            break
        except Exception as ex:
            msg_text = "Error occured while sending QT mail to Vivek and Abhishek.Please check immediately"
            print "Error: unable to send email"
            print "Error : " + str(ex)
            print "*" * (100)
            print "Retrying ............................"


try:
    print "Sending SMS to +919890233404"
    account_sid = "ACbdbd2096786b69584c4a8b2de34d38ea"
    auth_token = "1efa1a6cd0f90347ec2aaea6a6a79dbe"
    client = twilio.rest.TwilioRestClient(account_sid, auth_token)
    msg_text = "Hi Nirbhay!\n"+msg_text 
    message = client.messages.create(
        body=msg_text,
        to="+919890233404",
        from_="+18185930626"
    )
    print "Message sending completed"
except twilio.TwilioRestException as e:
    print "Error occurred while sending message"
    print e
except Exception as e:
    print "asasdsadsad"
    print e
# print "asdasdsadsad"
# from sendsms import api
# api.send_sms(body='I can haz txt', from_phone='+41791111111', to=['+41791234567'])

# try:
#     import ipdb
#     ipdb.set_trace()
#     numbers = ['9890233404']
#     if x!=4:
#         message = "Hi Nirbhay, QT mail was sent suceessfully"
#     else:
#         message = "Oops,Something went wrong in mail sending"
#     send_confirm(numbers, message)
# except Exception as ex:
#         print "Error: Message sending failed"
#         print "Error : " + str(ex)
