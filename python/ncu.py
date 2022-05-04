#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
import time
import os
from mail import sendMailtoqq

# 使用说明：设置了Token和SMTP对应的环境变量和需要发送的QQ号后就可以使用了
# 环境变量：
# NCU_TOKEN: 提取的Token

# 通过Token获取学号并登入


class Student:
    def __init__(self, token, qq) -> None:
        self.token = token
        self.qq = qq
        pass


def getUID(token):
    url_login = 'http://jc.ncu.edu.cn/system/auth/loginByToken'
    headers = {'Host': 'jc.ncu.edu.cn',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/90.0.4430.93', 'token': token}
    # 通过token登录
    loginToken_json = requests.post(url_login, headers=headers).json()
    print(loginToken_json['data']['userName'],
          loginToken_json['data']['userId'])
    # 通过获取到的学号来打卡，如果没获取到学号则返回error
    try:
        uid = loginToken_json['data']['userId']
        return uid
    except TypeError as emsg:
        return "error"


# 通过学号和Token来提交打卡信息
def signIn(uid, token):
    if uid == "error":
        return "打卡失败"
    # 成功传入学号，开始打卡
    url_sign = 'http://jc.ncu.edu.cn/gate/student/signIn'
    headers = {'Host': 'jc.ncu.edu.cn',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/90.0.4430.93', 'token': token}
    info = {'addressCity': "南昌市", 'addressInfo': "江西省南昌市", 'addressProvince': "江西省", 'closeHb': "否", 'closeIll': "否", 'healthDetail': "无异常", 'healthStatus': "无异常", 'inChina': "是",
            'isGraduate': "否", 'isIll': "否", 'isIsolate': "否", 'isIsolation': "否", 'isolatePlace': "无", 'isolationPlace': "无", 'temperature': 0, 'temperatureStatus': "正常", 'userId': uid}
    # 通过传入的uid签到
    sign_json = requests.post(url_sign, headers=headers, data=info).json()
    print(sign_json)
    return sign_json['message']


# 设置邮件服务器信息

def checkIn(student):
    # 获取学号
    uid = getUID(student.token)
    # 打卡
    sign_info = signIn(uid, student.token)
    # 发送邮件
    sendMailtoqq(sign_info, student.qq)
    return sign_info


Example = Student(os.environ['token'], os.environ['qq'])
time.sleep(5)
