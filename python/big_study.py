#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
import json
import time
from mail import sendMailtoqq
from anti_useragent import UserAgent
import secrets


class student:
    def __init__(self, NumID, CARDNo, qq) -> None:
        self.NumID = NumID
        self.CARDNo = CARDNo
        self.qq = qq
        pass


def makeHeader():
    return {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Connection': 'close',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'JSESSIONID=' + secrets.token_urlsafe(40),
        'Host': 'www.jxqingtuan.cn',
        'Origin': 'http://www.jxqingtuan.cn',
        'User-Agent': UserAgent(platform="iphone").wechat,
        'X-Requested-With': 'XMLHttpRequest'
    }


def getCourse():
    url = "http://www.jxqingtuan.cn/pub/vol/volClass/current"
    CourseJson = requests.get(url, headers=makeHeader()).json()
    Course = CourseJson.get("result")
    print(Course)
    try:
        if json.dumps(Course).count("id") == 1:
            return Course.get("id")
        else:
            return Course[-1].get("id")
    except:
        print("查询课程致未知错误")
        exit()


courseID = getCourse()


def getStudy(student):
    url = "http://www.jxqingtuan.cn/pub/vol/volClass/join?accessToken="
    data = {"course": courseID, "nid": student.NumID, "cardNo": student.CARDNo}
    res = json.loads(
        (requests.post(url=url, data=json.dumps(data), headers=makeHeader())).text)
    print(res)
    if res.get("status") == 200:
        sendMailtoqq("青年大学习已完成", student.qq)
    else:
        sendMailtoqq("青年大学习失败", student.qq)


eg = student("nid", "info", "qq")

getStudy(eg)
time.sleep(5)
