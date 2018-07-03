#!/usr/bin/python
import dns.resolver
import os
import http
def checkip(ip):
    getcontent = ""
    conn = http.client.HTTPConnection(ip, 80, timeout=10)  # 创建http连接对象,定义http连接超时时间(10秒)
    conn.request("GET", "/", headers={"Host": "www.g-i.asia"})  # 发起URL请求,添加host主机头
    r = conn.getresponse()
    getcontent = r.status  # 获取URL页面前15个字符，以便做可用性校验
    print(getcontent)
checkip("106.14.162.74")