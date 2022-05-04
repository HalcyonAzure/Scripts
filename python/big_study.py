#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
import json
import time
from mail import sendMailtoqq


class student:
    def __init__(self, NumID, CARDNo, qq) -> None:
        self.NumID = NumID
        self.CARDNo = CARDNo
        self.qq = qq
        pass


def getCourse():
    url = "http://osscache.vol.jxmfkj.com/html/assets/js/course_data.js"
    res = requests.get(url).text
    CourseInfo = res[18:]
    CourseJson = json.loads(CourseInfo)
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
    url = "http://osscache.vol.jxmfkj.com/pub/vol/volClass/join?accessToken="
    data = {"course": courseID, "nid": student.NumID, "cardNo": student.CARDNo}
    res = json.loads((requests.post(url=url, data=json.dumps(data))).text)
    print(res)
    if res.get("status") == 200:
        sendMailtoqq("青年大学习已完成", student.qq)
    else:
        sendMailtoqq("青年大学习失败", student.qq)


eg = student("nid", "info", "qq")

getStudy(eg)
time.sleep(5)
