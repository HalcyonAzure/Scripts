#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
import os
from mail import sendMailtoqq


class ssrInfo:
    def __init__(self, ssr_email, ssr_passwd) -> None:
        self.ssr_email = ssr_email
        self.ssr_passwd = ssr_passwd
        pass


eg = ssrInfo(os.environ['mail'], os.environ['passwd'])


def ssrCheck(ssrInfo):
    # SSPanel主体
    url_login = "https://xn--gmqz83awjh.moe/auth/login"
    body = {'email': ssrInfo.ssr_email,
            'passwd': ssrInfo.ssr_passwd, 'remember_me': 'on', }

    # 通过Cookie登入
    logingIn = requests.session()  # 初始化session
    logingIn.post(url_login, data=body)  # 提交post请求，获取session具体信息
    cookieJar = requests.sessions.RequestsCookieJar()  # 初始化CookieJar
    logingIn.cookies.update(cookieJar)  # 将session获得的cookie更新到CookieJar
    cookie = logingIn.cookies.get_dict()  # 将CookieJar的内容转为字典输出
    res = requests.post(
        'https://xn--gmqz83awjh.moe/user/checkin', cookies=cookie).json()
    return res


if __name__ == '__main__':
    # 通过Cookie签到
    res = ssrCheck(eg)
    sendMailtoqq(res['msg'], os.environ['qq'])
