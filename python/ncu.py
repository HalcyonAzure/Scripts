#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from re import M
import requests
import json
import os
from sign_lib import sendMailtoqq

# 使用说明：设置了Token和SMTP对应的环境变量和需要发送的QQ号后就可以使用了
# 环境变量：
# NCU_TOKEN: 提取的Token
# QQ: 需要发送的QQ号
# SMTP_HOST: 邮件服务器地址
# SMTP_USER: 邮件服务器用户名
# SMTP_PASS: 邮件服务器密码


# 通过Token获取学号并登入
def getUID(token):
    url_login = 'http://jc.ncu.edu.cn/system/auth/loginByToken'
    headers = {'Host': 'jc.ncu.edu.cn', 'token': token}
    # 通过token登录
    loginToken_json = requests.post(url_login, headers=headers).json()
    print(loginToken_json)
    # 通过获取到的学号来打卡，如果没获取到学号则返回error
    try:
        uid = loginToken_json['data']['userId']
        return uid
    except TypeError as emsg:
        return "获取学号失败"


# 通过学号和Token来提交打卡信息
def signIn(uid, token):
    if uid == "error":
        return "打卡失败"
    # 成功传入学号，开始打卡
    url_sign = 'http://jc.ncu.edu.cn/gate/student/signIn'
    headers = {'Host': 'jc.ncu.edu.cn', 'token': token}
    info = {'addressCity': "南昌市", 'addressInfo': "江西省南昌市", 'addressProvince': "江西省", 'closeHb': "否", 'closeIll': "否", 'healthDetail': "无异常", 'healthStatus': "无异常", 'inChina': "是",
            'isGraduate': "否", 'isIll': "否", 'isIsolate': "否", 'isIsolation': "否", 'isolatePlace': "无", 'isolationPlace': "无", 'temperature': 0, 'temperatureStatus': "正常", 'userId': uid}
    # 通过传入的uid签到
    sign_json = requests.post(url_sign, headers=headers, data=info).json()
    print(sign_json)
    return sign_json['message']


if __name__ == '__main__':
    # 打卡
    uid = getUID(os.environ['NCU_TOKEN'])
    req_msg = signIn(uid, os.environ['NCU_TOKEN'])

    # 通过服务器给目标QQ发送邮件
    sendMailtoqq(req_msg, os.environ['QQ'], os.environ['SMTP_HOST'],
                 os.environ['SMTP_USER'], os.environ['SMTP_PASS'])
