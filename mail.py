from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import email.utils

def send_mail(to, subject, body):
    ID = 's.takisawa.sys22@morijyobi.ac.jp'
    PASS = os.environ['MAIL_PASS']
    HOST = 'smtp.gmail.com'
    PORT = 587
    
    # MIME インスタンス
    msg = MIMEMultipart()
    
    msg.attach(MIMEText(body, 'html'))
    
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr(('システム',ID))
    msg['To'] = email.utils.formataddr(('ユーザ様',to))
    
    #mailを送る処理
    server = SMTP(HOST,PORT)
    server.starttls()
    
    server.login(ID,PASS) # サーバーへのログイン処理
    server.send_message(msg) # メールを送信
    server.quit()