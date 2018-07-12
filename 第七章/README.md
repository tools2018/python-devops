#《Python自动化运维：技术与最佳实践》附带示例及案例源码

##第七章 目录说明
+ fabric - fabric3模块示例
pip install Fabric3

fabric 依赖第三方 setuptools，crypto，paramiko，所以推荐使用 pip3 安装，会自动匹配依赖包。注意是 fabric3。

如果使用 pip3 install fabric ，在导入的之后执行的时候会有问题。

fab 语法

fab 是 fabric 程序的命令行入口，在命令行使用！！！，语法：

fab [options] <command>[arg1,arg2:val2,host=foo]

fab 命令的执行，默认依赖一个 fabfile.py 的文件，可以对该文件进行编辑，也可以执行其他的文件，用 -f 参数指定文件即可。

fab 参数

可以使用 fab -help 查看具体参数：

-l,     显示定义好的任务函数名
-f,     指定 fab 入口文件，默认 fabfile.py
-g,     指定网关设备，比如堡垒机环境，填写堡垒机 ip 即可
-H， 指定目标主机，多台用逗号隔开
-P      以异步并行方式运行多主机任务，默认串行运行
-R， 指定 role，以角色名区分不同业务组设备
-t      设置设备连接超时时间
-T      设置远程主机命令执行超时时间
-w      当命令失败的时候，发出警告，而不是终止任务
-p      指定密码

fabric 常用 api

fabric 执行本地命令和远程命令，必须先导入 fabric 对应的 api 接口。
常用 api

local       执行本地命令
lcd         切换本地目录

cd          切换远程目录
run         执行远程命令
sudo        sudo 方式执行远程命令
put         上传本地文件到远程主机
get         从远程主机下载文件到本地
prompt      获得用户输入信息
confirm     获得提示信息确认
reboot      重启远程主机

@task       函数修饰符，标识的函数为 fab 可调用的，不标记的对 fab 不可见。
@runs_once  函数修饰符，标识的函数只会执行一次，不受多台主机影响
@roles， 函数修饰符，配合 env.roledefs 的角色使用

@task 函数修饰符在下面的实验中并没有试验出结果，即便不是调用默认 fabric.py 中的函数，也无需使用 @task 函数修饰符，直接调用 fun 函数的名称即可。

api 调用方法

from fabric.api import *
env.hosts = 'localhost'

def hello():
    local('echo hello world')

def check():
    local('ls /Users/')

def remote():
    run('ping www.baidu.com')

env 全局环境变量

导入 env 变量

from fabric.api import evn

env.hosts,  定义目标主机，多个主机用列表的形式体现
env.exclude_hosts,  排除指定的主机，env.exclude_hosts=['192.168.184.2']

env.user,   定义用户名
env.port，   定义目标主机端口

env.password，   定义密码
env.passwords,  与 password 功能一样，需要指定主机。env.passwords = {'user1@host':'password','user2@host':'password'}

env.gateway,    定义网关（中转、堡垒机）IP

env.roledefs,   定义角色分组。env.roledefs = {'webserver':['host1','host2'], 'dbserver':['db1','db2']}

env.deploy_release_dir  自定义全局变量，env.deploy_release_dir, env.age, env.sex 等等

示例

fab 依赖的 fabric.py 文件中创建函数。

import fabric.api

def hello():
    fabric.api.local('echo hello world')

def check():
    fabric.api.local('ls /Users/')

def remote():
    fabric.api.run('ping www.baidu.com')

在命令行执行命令的时候，使用 fab + fun函数即可。

$ fab hello
$ fab check

指定其他文件调用 fabric

from fabric.api import local, lcd
import os

def hello():
    print('hello sucre')

def cwd():
    dir = os.getcwd()
    print(dir)

执行远程命令

fab 最牛的功能，就是可以在远程主机上执行命令。

from fabric.api import *

env.user = 'root'
env.hosts = ['192.168.184.2', '192.168.184.22']
env.password = 'yourpassword'
env.passwords = {
    'staging': '11111',
    'build': '123456'
}
env.roledefs = {
    'webserver': ['bjhee@example1.com','bjhee@example2.com'],
    'dbserver': ['build@example3.com']
}

@roles('webserver')
def remote_task():
    with cd('/data/logs'):     # with 的左右是让后面的表达式，继承前面的状态
        run('ls -l')           # 实现 'cd /data/logs/ && ls -l' 的效果

@roles('dbserver')
def remote_build():
    with cd('/tmp/citizen_wang'):
        run('git pull')

def remote_deploy():
    run('tar zxvf /tmp/fabric.tar.gz')
    run('mv /tmp/fabric/setup.py /home/www/')

def task():
    execute(remote_build)
    execute(remote_deploy)

命令行调用：

$ fab task
$ fab remote_build
$ fab -R webserver deploy  # 指定 build 角色执行 deploy 命令

put、get 语法

get('/remote/path/filename', '/local/path/filename')

put('/local/path/filename','/remote/path/filename'[, use_sudo=True])

reboot(wait=60)