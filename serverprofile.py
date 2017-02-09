from serveralarm import ServerAlarm
from sendmail import SENDMAIL

EMAIL_SUBJECT = "REPORT ALL SYSTEM BY KHANHNN"
EMAIL_FROM = 'alert-system@khanhnn.com.vn'
EMAIL_RECEIVER = ['khanhnn@khanhnn.com.com.vn', ]
SERVER_SMTP = "8.8.8.8"
SERVER_SMTP_PORT = 25
TEXT_SUBTYPE = "html"
EMAIL_PASS = '123456'
EMAIL_CONTENT_HEAD = '''
<html>
    <style type="text/css">
        .red{ color: red; }
        .blue{ color: blue; }
    </style>
    <body>
	Thong tin nhu sau: '''

allserver = [
{"ip": "192.168.1.1", "uname": "khanhnn", "pwd": "123456"},
]

contents = [EMAIL_CONTENT_HEAD]
srv = ServerAlarm()
for s in allserver:
    srv.connect(s['ip'], s['uname'], s['pwd'])
	
    contents.append('''<table border='1' style='width: 88%;text-align: left;'><caption><h2 class='blue'>{0}</h2></caption>
    <tr><th>CONNECT MESSAGE</th><th>DISK SPACE USAGE</th></tr>'''.format(s['ip']))
    contents.append('''<tr><td>{0}</td><td>{1}</td></tr>'''.format(str(srv.error), str(srv.getdiskspace()) ))
    contents.append('''</table>''')

contents = ''.join(contents)
m = SENDMAIL()
m.send(EMAIL_FROM, EMAIL_RECEIVER, contents, EMAIL_SUBJECT, EMAIL_PASS)
