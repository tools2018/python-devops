#!/usr/bin/env python
import paramiko
import os,sys,time

hostname = "172.16.1.12"
username = "root"
password = "123"

blip = "172.16.1.12"
bluser = "root"
blpasswd = "123"

port = 22
passinfo = '\'s password: '
paramiko.util.log_to_file('syslogin.log')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=blip, username=bluser, password=blpasswd)


#new session
channel = ssh.invoke_shell()
channel.settimeout(10)

buff = ''
resp = ''
channel.send('ssh '+username+'@'+hostname+'\n')

while not buff.endswith(passinfo):
    try:
        resp = channel.recv(9999)
        print(resp)
    except Exception as e:
        print('Error info:%s connection time.' % (str(e)))
        channel.close()
        ssh.close()
        sys.exit()
    buff = str(resp)
    if not buff.find('yes/no') == -1:
        channel.send('yes\n')
    buff = ''

channel.send(password+'\n')

buff = ''
while not buff.endswith('# '):
    resp = channel.recv(9999)
    if not resp.find(passinfo) == -1:
        print('Error info: Authentication failed.')
        channel.close()
        ssh.close()
        sys.exit() 
    buff += str(resp)

channel.send('ifconfig\n')
buff = ''
try: 
    while buff.find('# ') == -1:
        resp = channel.recv(9999)
        buff += str(resp)
except Exception as e:
    print("error info:"+str(e))

print(buff)
channel.close()
ssh.close()
