#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import sys
import os
#sys.path.append('./')
#print sys.path
import definition
from config import config
from lib.logConf import logConf
from lib.logutils import logutils

#TODO list:
#1. find pid by words
#1.1 pid may change, process restart
#2. unittest
#3. decode flow
#4. display

class mflow():
    def __init__(self, logname='', outdir='./', loglevel='DEBUG'):
        self.log = os.path.realpath(logname)
        with open(self.log, 'rb') as logfile:
            self.loglines = logfile.readlines()
        self.logger = logConf(debuglevel=loglevel)
        self.logger.logger.info('init flow')
        self.config = config()
        self.logutils = logutils()
        self.pid = list()

    def findPid(self):
        '''
        description: process may restart, so pid is a list
        :return:
        '''
        mpattern = self.config.getmkey()
        for index, line in enumerate(self.loglines):
            fields = line.split()
            fruit = self.logutils.findfields(fields)
            pid = fruit['pid']
            if pid not in self.pid and self.logutils.patterninline(mpattern, line):
                self.logger.logger.info('found media engine id ' + str(pid))
                self.pid.append(pid)



if __name__ == '__main__':
    mflow = mflow(logname="./samplelog/main.log")
    mflow.findPid()
    pass
