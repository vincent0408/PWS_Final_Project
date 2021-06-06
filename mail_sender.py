import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import os

#設定寄件給同學的email帳號

#path = r'C:/Users/Vincent/Desktop/PWS Homework//'
#df = pd.DataFrame()
#for filename in os.listdir(path):
#    hw = pd.read_csv(path + filename, usecols = [7], names=['Author'], header=None)
#    df = pd.concat([df, hw])
#students = df['Author'].unique().tolist()
#students[students.index('b06302345@ntu.edu.tw')] = 'b06302345'
#students.remove('jeffery12697')
#students.remove('yeutong00')
#students.remove('hyusterr')

students = ['b06702026']

def getEmail(student):
    link = 'https://doodoolu.github.io/'
    subject = '[PWS Final Project] 誰是佼佼者!!!'
    contents = """
{} 您好，\n
我們是第幾組，本次期末專案我們利用Python對ccClube Judge進行分析，
\n將每次作業繳交狀況進行分析後，歡迎大家透過我們的網站查看你/妳這學期的表現！
\n在這個班上，誰是佼佼者? 快點擊下方連結看看是不是你吧！
    
網站連結： {}
預設帳號： {}
預設密碼： {}

誰是佼佼者團隊敬上

*若您已經退選或是停修本門課程請忽略此信，很抱歉造成您的不便
    """.format(student, link, student, student)    
    
    # 開始組合信件內容
    mail = MIMEMultipart()
    mail['From'] = from_address
    mail['To'] = to_address
    mail['Subject'] = subject

    #將信件內文加到email中
    mail.attach(MIMEText(contents))
    return mail

#寄件者使用的 Gmail帳戶 資訊
gmail_user = 'pwsfinalproject@gmail.com'
gmail_password = 'pwsfinal2021'
from_address = gmail_user
    
# 設定smtp伺服器並寄發信件    
smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)
for student in students:
    to_address = student + '@ntu.edu.tw'
    mail = getEmail(student)
    smtpserver.sendmail(from_address, to_address, mail.as_string())
smtpserver.quit()





