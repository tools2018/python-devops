#!/usr/bin/env python

from fabric.api import *

env.user = 'root'
env.hosts = ['172.16.1.12', '172.16.1.15']
env.password = '123'

@runs_once
def local_task():
    local("uname -a")

def remote_task():
    with cd("/data/logs"):
        run("ls -l")
