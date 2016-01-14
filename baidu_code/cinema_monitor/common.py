__author__ = 'yezhihua'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import time

uidcrypt =  os.path.abspath(os.path.dirname(__name__)) + '/uid_crypt'

NUOMI_PREFIX = 'http://www.nuomi.com/cinema/'
#http://www.nuomi.com/pcindex/main/timetable?cinemaid=3574080d5096fa5a774ff1e02&mid=9414&needMovieInfo=1&tploption=1&_=1427738974387
TIMETABLE_URL = 'http://www.nuomi.com/pcindex/main/timetable?'

NORMAL_LOG = 'normal'

def runShell(shell):
    result = subprocess.Popen(shell, shell=True,stdout=subprocess.PIPE).stdout.read()
    result = result.split('\n')[0]
    return result

def encodebid(orig):
    shell = 'echo -n ' + str(orig) + '|./uid_crypt encode'
    bid = runShell(shell)
    return bid

def getSeconds():
    shell = "date +%s"
    sec = runShell(shell)
    return sec

