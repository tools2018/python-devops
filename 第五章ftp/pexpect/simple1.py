#!/usr/bin/env python3
import paramiko
import pprint

def ssh2(ip,port,username,passwd,timeout=10,cmd='ls',*key_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22,username,passwd)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    pprint.pprint(stdout.read().decode('utf-8').split('\n'))

if __name__ == '__main__':
    ip = input('ip: ')
    username = input('username: ')
    password = input('password: ')
    ssh2(ip, '22', username, password, cmd='uptime')
