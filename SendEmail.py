import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

def send_email(SMTP_host,from_account,from_password,to_account,subject,content,attc_name,attc_file):
    smtp=smtplib.SMTP(SMTP_host)

    smtp.connect(SMTP_host, 587)
    smtp.starttls()
    smtp.login(from_account,from_password)

    msg=MIMEMultipart()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    msg['Subject']=Header(subject,'utf-8')
    msg['From']=from_account
    msg['To']=to_account

    xlsx=MIMEApplication(open(attc_file,'rb').read())
    xlsx['Content-Type']='application/octet-stream'
    xlsx.add_header('Content-Disposition','attachment',filename=attc_name)
    msg.attach(xlsx)

    smtp.sendmail(from_account,to_account,msg.as_string())

    smtp.quit()