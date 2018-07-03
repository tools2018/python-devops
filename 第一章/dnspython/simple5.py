#!/usr/bin/python
import dns.resolver
import os
import http

iplist=[]    #定义域名IP列表变量
appdomain="www.gwantsi.com"    #定义业务域名

def get_iplist(domain=""):    #域名解析函数，解析成功IP将追加到iplist
    try:
        A = dns.resolver.query(domain, 'A')    #解析A记录类型
    except Exception as e:
        print("dns resolver error:"+str(e))
        return
    for i in A.response.answer:
        for j in i.items:
            iplist.append(j.address)    #追加到iplist
    return True

def checkip(ip):
    conn = http.client.HTTPConnection(ip, 80, timeout=10)  #创建http连接对象,定义http连接超时时间(10秒)
    try:
        conn.request("GET", "/", headers={"Host": appdomain})  #发起URL请求,添加host主机头
        r = conn.getresponse()
        getcontent = r.status   #获取URL状态，以便做可用性校验
    finally:
        if getcontent == 200:  #监控URL页的内容一般是事先定义好，比如“HTTP200”等
            print(ip+" [OK]")
        else:
            print(ip+" [Error]")    #此处可放告警程序，可以是邮件、短信通知

if __name__=="__main__":
    if get_iplist(appdomain) and len(iplist) > 0:    #条件：域名解析正确且至少要返回一个IP
        for ip in iplist:
            checkip(ip)
    else:
        print("dns resolver error.")
