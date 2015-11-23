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
    sender = 'tushar.thorat@firstcry.com'
    #receivers = ['nirbhayk@leotechnosoft.net','abhisheks@leotechnosoft.net','vivekj@leotechnosoft.net','james@trans-asia.co.jp']
    #receivers = ['nirbhayk@leotechnosoft.net','vivekj@leotechnosoft.net']
    receivers = ['nirbhayk@leotechnosoft.net',]
    msg = MIMEMultipart()
    cur_date = "%d" %now.day
    cur_month = "%d" %now.month
    cur_year = "%d" %now.year

    dt = str(cur_date) + " " + now.strftime('%b') + " " + cur_year
    msg['Subject'] = 'Work report as on dated {}'.format(dt)
    #msg['From'] = 'nirbhayk@leotechnosoft.net'
    msg['From'] = 'tushar.thorat@firstcry.com'
    msg['To'] = 'james@trans-asia.co.jp'
    msg['Cc'] = 'abhisheks@leotechnosoft.net, nirbhayk@leotechnosoft.net'
    txt = """Hi Sir,
    
Kindly find attached work report as on dated {}
    
-- 
Thanks
Tushar
    """.format(dt)
    fl_name = str(cur_date) + "_" + now.strftime('%b') + "_" + cur_year + "_" + "Tasksheet.xls"
    import ipdb;ipdb.set_trace()
    path = "/home/phaniv/Desktop/QT_Timesheet/" + cur_year + "/" + now.strftime('%B') + "/" + fl_name
    if not os.path.exists("/home/phaniv/Desktop/QT_Timesheet/" + cur_year + "/" + now.strftime('%B') + "/"):
        os.mkdir("/home/phaniv/Desktop/QT_Timesheet/" + cur_year + "/" + now.strftime('%B') + "/")
    txt = txt.format(str(cur_date + " " + now.strftime('%B') + " " + cur_year ))
    msg.attach(email.mime.Text.MIMEText(txt))  
    smtpObj = smtplib.SMTP('smtp.firstcry.com')
    smtpObj.login("tushar.thorat@firstcry.com", "Goodlife@123")
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
            msg_text = "Timesheet mail has been successfully sent."
            print "Mail Sent Suceesfully"
            break
        except Exception as ex:
            msg_text = "Error occured while sending timesheet mail. Please check immediately"
            print "Error: unable to send email"
            print "Error : " + str(ex)
            print "*" * (100)
            print "Retrying ............................"


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
