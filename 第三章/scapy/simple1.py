# -*- coding: utf-8 -*-
import os,sys,time,subprocess
import warnings,logging

warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import traceroute

domains = input('Please input one or more IP/domain: ')
target = domains.split(' ')
dport = [80]
if len(target) >= 1 and target[0] != '':
    res, unans = traceroute(target, dport=dport, retry=-2)
    res.graph(target="> test.svg")
    time.sleep(1)
    subprocess.Popen("/usr/bin/convert test.svg test.png", shell=True)
    # subprocess.Popen("/c/Windows/system32/convert test.svg test.png", shell=True)
else:
    print("IP/domain number of errors,exit")
