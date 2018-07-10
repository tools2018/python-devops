#!/usr/bin/env python
import paramiko
import os

hostname = '172.16.1.12'
username = 'root'
paramiko.util.log_to_file('syslogin.log')

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
privatekey = os.path.expanduser('/c/Users/Ceph/.ssh/id_rsa')
key = paramiko.RSAKey.from_private_key_file(privatekey)

ssh.connect(hostname=hostname, username=username, pkey=key)
stdin, stdout, stderr = ssh.exec_command('df -h')
print(stdout.read())
ssh.close()
