#!/usr/bin/python
import csv
import xlwt
import datetime
import MySQLdb
import twilio
import twilio.rest


class no_record_error(Exception):
    pass

def create_xl():
    # Open database connection
    global msg_text 
    db = MySQLdb.connect("172.16.0.62","root","root","helpdesk" ,3306)
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # execute SQL query using execute() method.
    # query = "select * from hesk_tickets limit 1 ;"
    # fl_name = "HR.xls"
    now = datetime.datetime.now()
    fl_name = str(now.strftime("%d_%a_%Y")) + ".xls"
    
#     query = "select dt,trackid,name,subject,CASE status when '3' then 'Done' ELSE 'Pending' END from hesk_tickets where owner=10  and  (dt =  CURDATE() or lastchange = CURDATE()"
    query = "select dt,trackid,name,subject,message,CASE status when '3' then 'Done' ELSE 'Pending' END from hesk_tickets where owner=10  and ((status='3' and lastreplier='1' and lastchange >= CURDATE()) or ( status = '0' ));"
    path = "/home/chaitanyas/Desktop/Tushar_thorat/Daily_report/" + fl_name
    path = "/home/phaniv/Desktop/Daily_report/" + fl_name
    print path
    cursor.execute(query)
    
    
    s1 = xlwt.Workbook(encoding="utf-8")
    # sheets = s1.set_active_sheet(0)
    # sheets = s1.get_sheet(0)
    sheets = s1.add_sheet("Ticket list",cell_overwrite_ok=True)
    n = 0
    first = ['Sr.no','Date','Ticket ID','User','Subject','Details', 'Status', 'Time taken']
    data = cursor.fetchall()
    if len(data) == 0:
        raise no_record_error
    for i,rows in enumerate(data):
        sheets.write(i+1,0,str(i+1))
        for j,cols in enumerate(rows):
            if type(cols) is datetime.datetime:
                cols = str(cols.strftime("%d-%a-%Y"))
            sheets.write(i+1,j+1,str(cols))
    
    sheets.col(first.index('Details')).width = 256*70
    sheets.col(first.index('Subject')).width = 256*40
    sheets.col(first.index('Ticket ID')).width = 256 * 20
    style = xlwt.XFStyle()
    style.font.bold = True
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_background_colour = xlwt.Style.colour_map['gray50']
    style.pattern = pattern
    for i,x in enumerate(first):
        sheets.write(0,i,first[i],style)
    s1.save(path)    
    print data
    
    # disconnect from server
    db.close()


now = datetime.datetime.now()
d = now.strftime("%a")
day_text = "Today is " + str(now.strftime("%A"))
print day_text
if d.upper() in ['SAT','SUN']:
    print "No need to create Excel file"
    msg_text = day_text + ".\nNo need create excel file"
else:
    for x in range(1,5):
        try:
            msg_text = "Excel file created please fill time details"
            create_xl()
            print "Excel file created suceessfully"
            break
        except no_record_error as ex:
            print "No records found"
            msg_text = "No records found while creating excel file"
            break
        except Exception as ex:
            print "Excel sheet creation failed,\n Retrying ",
            msg_text = "Error occured while creating excel file.Please check immediately"
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
        print "Message sending completed for excel file"
        break
    except Exception as ex:
        print "Error occurred while sending message file"
        print ex
print msg_text

