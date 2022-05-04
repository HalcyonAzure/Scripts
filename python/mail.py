#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import smtplib
import os
from email.mime.text import MIMEText


# 给特定QQ发送邮件
# msg: 要发送的信息
# qq: 要发送的QQ号
def sendMailtoqq(msg, qq):
    receiver = [qq + '@qq.com']

    print(msg)
    message = MIMEText(msg, 'plain', 'utf-8')
    message['Subject'] = '邮件提醒'
    message['From'] = "Reminder<" + os.environ['SMTP_USER'] + ">"
    message['To'] = "Reminder<" + receiver[0] + ">"

    try:
        smtpObj = smtplib.SMTP_SSL(os.environ['SMTP_HOST'])
        smtpObj.login(os.environ['SMTP_USER'], os.environ['SMTP_PASS'])
        smtpObj.sendmail(os.environ['SMTP_USER'],
                         receiver, message.as_string())
        smtpObj.quit()
        print('发送成功')
    except smtplib.SMTPException as e:
        print('发送失败', e)
