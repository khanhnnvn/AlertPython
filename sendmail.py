import email,email.encoders,email.mime.text,email.mime.base
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from smtplib import SMTP
from email.utils import COMMASPACE, formatdate
from datetime import date, timedelta
import os

SERVER_SMTP = "8.8.8.8"
SERVER_SMTP_PORT = 25
TEXT_SUBTYPE = "html"
EMAIL_PASS = '123456'
EMAIL_FROM = 'khanhnnn@khanhnn.com.com.vn'
EMAIL_RECEIVER = ['khanhnn@khanhnn.com.com.vn']

class SENDMAIL(object):
    """docstring for SENDMAIL"""
    def __init__(self, server=SERVER_SMTP, port=SERVER_SMTP_PORT):
        super(SENDMAIL, self).__init__()
        self.server = server
        self.port = port

    def __del__(self):
        pass

    def send(self, sender, receivers, content, subject='', pswd=EMAIL_PASS, filex='', txttype=TEXT_SUBTYPE):
        #Create the email.
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ','.join(receivers)
        msg['Date'] = formatdate(localtime=True)
        body = MIMEMultipart('alternative')
        body.attach(MIMEText(content, txttype ))
        #Attach the message
        msg.attach(body)

        #Attach a excel file if exists
        if filex != '':
            fp = open(filex, 'rb')
            file1=email.mime.base.MIMEBase('application','vnd.ms-excel')
            file1.set_payload(fp.read())
            fp.close()
            email.encoders.encode_base64(file1)
            NAME_ATTACH = "attachment;filename=" + os.path.basename(filex)
            file1.add_header('Content-Disposition',NAME_ATTACH)
            msg.attach(file1)

        #begin sendmail
        try:
            smtpObj = SMTP(self.server, self.port)
            smtpObj.ehlo()
            smtpObj.login(user=sender, password=pswd)
            smtpObj.sendmail(sender, receivers, msg.as_string())
            smtpObj.quit()
        except SMTPException as error:
            print "Error: unable to send email :  {err}".format(err=error)
        print "Send mail done!"

if __name__ == '__main__':
    m = SENDMAIL()
    m.send(EMAIL_FROM, EMAIL_RECEIVER, 'abc', subject='a test subject')
