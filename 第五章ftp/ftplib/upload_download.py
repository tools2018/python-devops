#!/usr/bin/env python3
# coding=utf-8
'''''
    ftp自动下载、自动上传脚本，可以递归目录操作
'''

from ftplib import FTP
import os, sys, time
import socket
import hashlib

class MYFTP:
    def __init__(self, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = remotedir
        self.port = port
        self.ftp = FTP()
        self.file_list = []
        # self.ftp.set_debuglevel(2)

    def __del__(self):
        self.ftp.close()
        # self.ftp.set_debuglevel(0)

    def login(self):
        ftp = self.ftp
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            print('开始连接到 %s' % (self.hostaddr))
            ftp.connect(self.hostaddr, self.port)
            print('成功连接到 %s' % (self.hostaddr))
            print('开始登录到 %s' % (self.hostaddr))
            ftp.login(self.username, self.password)
            print('成功登录到 %s' % (self.hostaddr))
            debug_print(ftp.getwelcome())
        except Exception:
            deal_error("连接或登录失败")
        try:
            ftp.cwd(self.remotedir)
        except(Exception):
            deal_error('切换目录失败')

    def is_same_size(self, localfile, remotefile):
        try:
            remotefile_size = self.ftp.size(remotefile)
        except:
            remotefile_size = -1
        try:
            localfile_size = os.path.getsize(localfile)
        except:
            localfile_size = -1
        debug_print('lo:%d  re:%d' % (localfile_size, remotefile_size), )
        if remotefile_size == localfile_size:
            return 1
        else:
            return 0

    def download_file(self, localfile, remotefile):
        if self.is_same_size(localfile, remotefile):
            debug_print('%s 文件大小相同，无需下载' % localfile)
            return
        else:
            debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % localfile)
            # return
        file_handler = open(localfile, 'wb')
        self.ftp.retrbinary('RETR %s' % (remotefile), file_handler.write)
        file_handler.close()

    def download_files(self, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except:
            debug_print('目录%s不存在，继续...' % remotedir)
            return
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
        debug_print('切换至目录 %s' % self.ftp.pwd())
        self.file_list = []
        self.ftp.dir(self.get_file_list)
        remotenames = self.file_list
        # print(remotenames)
        # return
        for item in remotenames:
            filetype = str(item[1]).split(' ',1)[0]
            filename = str(item[1]).split(' ',1)[1].strip(' ')
            local = os.path.join(localdir, filename)
            if filetype == '<DIR>':
                if not os.path.isdir(local):
                    os.makedirs(local)
                self.download_files(local, filename)
            else:
                self.download_file(local, filename)
        self.ftp.cwd('..')
        debug_print('返回上层目录 %s' % self.ftp.pwd())

    def upload_file(self, localfile, remotefile):
        if not os.path.isfile(localfile):
            return
        if self.is_same_size(localfile, remotefile):
            debug_print('跳过[相等]: %s' % localfile)
            return
        file_handler = open(localfile, 'rb')
        self.ftp.storbinary('STOR %s' % remotefile, file_handler)
        file_handler.close()
        debug_print('已传送: %s' % localfile)

    def upload_files(self, localdir='./', remotedir='./'):
        if not os.path.isdir(localdir):
            return

        localnames = os.listdir(localdir)
        self.ftp.cwd(remotedir)
        newdir = os.path.join(remotedir, localdir.strip('./'))

        if not os.path.isdir(newdir):
            try:
                self.ftp.mkd(newdir)
            except:
                debug_print('目录已存在 %s' % newdir)

        # print(type(localdir.strip('./')))
        for item in localnames:
            src = os.path.join(localdir, item)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(item)
                except:
                    debug_print('目录已存在 %s' % item)
                self.upload_files(src, item)
            else:
                self.upload_file(src, item)
        self.ftp.cwd('..')

    def get_file_list(self, line):
        file_arr = self.get_filename(line)
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_filename(self, line):
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr

def debug_print(s):
    print(s)

def deal_error(e):
    timenow = time.localtime()
    datenow = time.strftime('%Y-%m-%d', timenow)
    logstr = '%s 发生错误: %s' % (datenow, e)
    debug_print(logstr)
    file.write(logstr)
    sys.exit()


if __name__ == '__main__':
    file = open("log.txt", "a")
    timenow = time.localtime()
    datenow = time.strftime('%Y-%m-%d', timenow)
    logstr = datenow
    # 配置如下变量
    hostaddr = '172.16.1.5'  # ftp地址
    username = 'hy'  # 用户名
    password = 'g'  # 密码
    port = 21  # 端口号
    rootdir_local = '.' + os.sep + 'bak/'  # 本地目录
    rootdir_remote = './'  # 远程目录
    rootfile_local = '1.txt'  # 本地文件
    rootfile_remote = '1.txt'  # 远程文件

    uploaddir_local = './'  # 本地目录
    uploaddir_remote = './'     # 远程目录
    uploadfile_local = 'log.txt'  # 本地文件
    uploadfile_remote = 'log.txt'  # 远程文件

    f = MYFTP(hostaddr, username, password, rootdir_remote, port)
    f.login()
    # #单个文件下载
    # f.download_file(rootfile_local, rootfile_remote)
    #
    # #多个文件下载，并在本地创建目录
    # f.download_files(rootdir_local, rootdir_remote + 'jk')
    #
    # #单个文件上传
    # f.upload_file(uploadfile_local, uploaddir_remote + 'jk/' + uploadfile_remote)

    #多个文件上传，并在远端创建目录
    f.upload_files(uploaddir_local + 'kl', uploaddir_remote + 'jk')

    #记录一下日志
    timenow = time.localtime()
    datenow = time.strftime('%Y-%m-%d', timenow)
    logstr += " - %s 成功执行了备份\n" % datenow
    debug_print(logstr)
    file.write(logstr)
    file.close()