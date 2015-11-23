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


# Open database connection

# prepare a cursor object using cursor() method

# execute SQL query using execute() method.
# query = "select * from hesk_tickets limit 1 ;"
class no_record_error(Exception):
    pass

def send_mail():
    now = datetime.datetime.now()
    fl_name = str(now.strftime("%d_%a_%Y")) + ".xls"
    path = "/home/chaitanyas/Desktop/Tushar_thorat/Daily_report/" + fl_name
    path = "/home/phaniv/Desktop/Daily_report/" + fl_name
    import os 
    if not os.path.exists(path):
        raise no_record_error
    s1 = xlrd.open_workbook(path)
    sheets = s1.sheet_by_index(0)
    html = """
    <style>
    table {
        font-family: verdana,arial,sans-serif;
        font-size:11px;
        color:#333333;
        border-width: 1px;
        border-color: #666666;
        border-collapse: collapse;
    }
    table th {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #dedede;
    }
    table td {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #ffffff;
    }
    </style>
    Hello mam<br><br> Please find daily report<br><br>
    <table>
    <table>
    """
    for rows in range(sheets.nrows):
        html += "<tr>"
        for cols in sheets.row_values(rows):
            if rows == 0:
                html += "<th><strong>" + str(cols) + "</strong></th>"
            else:
                html += "<td>" +str(cols) + "</td>"
        html += "</tr>"
    html += "</table><br><br>"
    html += "<footer>Thank's & Regards,<br><br>Tushar </footer>"
    
    
    sender = 'nirbhayk@leotechnosoft.net'
    # receivers = ['nirbhayk@leotechnosoft.net','abhisheks@leotechnosoft.net','vivekj@leotechnosoft.net']
    receivers = ['nirbhayk@leotechnosoft.net','tusharthorat@leotechnosoft.net']
    receivers = ['nirbhayk@leotechnosoft.net',]
    msg = MIMEMultipart()
    now = datetime.datetime.now()
    cur_date = "%d" %now.day
    cur_month = "%d" %now.month
    cur_year = "%d" %now.year
    t = 'Daily report ({})'
    msg['Subject'] = t.format(str(cur_date + " " + now.strftime('%B') + " " + cur_year ))
    msg['From'] = 'tusharthorat@leotechnosoft.net'
    msg['To'] = 'ramonaf@leotechnosoft.net'
    # msg['Cc'] = 'abhisheks@leotechnosoft.net'
    print html
    msg.attach(email.mime.Text.MIMEText(html,'html'))
    smtpObj = smtplib.SMTP('smtp.1and1.com')
    smtpObj.login("nirbhayk@leotechnosoft.net", "nirbhay@327")
    smtpObj.sendmail(sender, receivers, msg.as_string())


now = datetime.datetime.now()
d = now.strftime("%a")
day_text = "Today is " + str(now.strftime("%A"))
print day_text
if d.upper() in ['SAT','SUN']:
    print "No need to send Daily timesheet mail"
    msg_text = day_text + ".\nNo need to Daily timesheet mail"
else:
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
