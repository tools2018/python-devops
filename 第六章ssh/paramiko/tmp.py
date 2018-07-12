#/usr/bin/python
import paramiko, sys
hostname = "172.16.1.15"
username = "root"
password = "123"
port = 22
passinfo = '\'s password: '
buff = ''
resp = ''


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username=username, password=password)

#new session
channel = ssh.invoke_shell()
channel.settimeout(10)


channel.send('ssh '+username+'@'+hostname+'\n')

while not buff.endswith(passinfo):
    try:
        resp = channel.recv(9999)
        # print(resp)
        # sys.exit()
    except Exception as e:
        print('Error info:%s connection time.' % (str(e)))
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp.decode()
    print(buff)
    if not buff.find('yes/no') == -1:
        channel.send('yes\n')
        channel.send(password + '\n')
        channel.send('ifconfig\n')
        buff = ''
