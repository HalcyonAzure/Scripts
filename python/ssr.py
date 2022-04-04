#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from multiprocessing import set_start_method
import requests
import json
import os
from sign_lib import sendMailtoqq

# 环境变量：
# SSR_EMAIL: 少数人邮箱
# SSR_PASSWD: 少数人密码
# QQ: 需要发送的QQ号
# SMTP_HOST: 邮件服务器地址
# SMTP_USER: 邮件服务器用户名
# SMTP_PASS: 邮件服务器密码


def getCookie():
    # SSPanel主体
    url_login = "https://xn--gmqz83awjh.moe/auth/login"
    body = {'email': ssr_email, 'passwd': ssr_passwd, 'remember_me': 'on', }

    # 通过Cookie登入
    logingIn = requests.session()  # 初始化session
    postJson = logingIn.post(url_login, data=body)  # 提交post请求，获取session具体信息
    cookieJar = requests.sessions.RequestsCookieJar()  # 初始化CookieJar
    logingIn.cookies.update(cookieJar)  # 将session获得的cookie更新到CookieJar
    cookie = logingIn.cookies.get_dict()  # 将CookieJar的内容转为字典输出
    return cookie


def RequestCookie(cookie):
    url = 'https://xn--gmqz83awjh.moe/user/checkin'
    res = requests.post(url, cookies=cookie).json()
    return res


if __name__ == '__main__':
    # 少数人帐号密码
    ssr_email = os.environ['SSR_EMAIL']
    ssr_passwd = os.environ['SSR_PASSWD']

    # 通过Cookie签到
    res = RequestCookie(getCookie())
    print(res['msg'])

    # # 发送邮件
    sendMailtoqq(res['msg'], os.environ['QQ'], os.environ['SMTP_HOST'],
                 os.environ['SMTP_USER'], os.environ['SMTP_PASS'])
