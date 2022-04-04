#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import smtplib
import json
import requests
from email.mime.text import MIMEText


# 给特定QQ发送邮件
# msg: 要发送的信息
# qq: 要发送的QQ号
# mail_host: 邮件服务器地址
# mail_user: 邮件服务器用户名
# mail_pass: 邮件服务器密码
def sendMailtoqq(msg, qq, mail_host, mail_user, mail_pass):
    receiver = [qq + '@qq.com']

    print(msg)
    message = MIMEText(msg, 'plain', 'utf-8')
    message['Subject'] = '邮件提醒'
    message['From'] = "Reminder<" + mail_user + ">"
    message['To'] = "Reminder<" + receiver[0] + ">"

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receiver, message.as_string())
        smtpObj.quit()
        print('发送成功')
    except smtplib.SMTPException as e:
        print('发送失败', e)
