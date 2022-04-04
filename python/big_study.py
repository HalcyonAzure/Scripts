#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
import json
import os
from sign_lib import sendMailtoqq

# 使用说明：设置了NID和SMTP对应的环境变量和需要发送的QQ号后就可以使用了
# 环境变量：
# NID: 打卡的组织号
# CARDNo: 要打卡的名字和学号
# QQ: 需要发送的QQ号
# SMTP_HOST: 邮件服务器地址
# SMTP_USER: 邮件服务器用户名
# SMTP_PASS: 邮件服务器密码


# 通过Token获取学号并登入
def getStudy(course, nid, cardNo):
    url = "http://osscache.vol.jxmfkj.com/pub/vol/volClass/join?accessToken="
    data = {"course": course, "nid": nid, "cardNo": cardNo}
    res = json.loads((requests.post(url=url, data=json.dumps(data))).text)
    if res.get("status") == 200:
        return "青年大学习已完成"
    else:
        return "青年大学习完成失败"


# 获取课程id
def getCourse():
    url = "http://osscache.vol.jxmfkj.com/html/assets/js/course_data.js"
    res = requests.get(url).text
    CourseInfo = res[18:]
    CourseJson = json.loads(CourseInfo)
    Course = CourseJson.get("result")
    try:
        if json.dumps(Course).count("id") == 1:
            return Course.get("id")
        else:
            return Course[-1].get("id")
    except:
        print("查询课程致未知错误")
        exit()


if __name__ == '__main__':
    # 打卡
    req_msg = getStudy(getCourse(), os.getenv("NID"), os.getenv("CARDNo"))
    print(req_msg)
    # 通过服务器给目标QQ发送邮件
    sendMailtoqq(req_msg, os.environ['QQ'], os.environ['SMTP_HOST'],
                 os.environ['SMTP_USER'], os.environ['SMTP_PASS'])
