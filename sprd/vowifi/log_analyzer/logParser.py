#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
import sys
import glob
from configobj import ConfigObj,ConfigObjError

'''
two ways to track logs:
1. by pid, but process may stop, so pid changes
2. by log tags,  but tags can be trivial.
'''


class logParser():
    def __init__(self):
        try:
            configfile = 'config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.files = {}
            self.files['log'] = config['files']['log']
            self.files['process'] = config['files']['process']

            #if only str, convert to list
            if type(config['process']['juphoon']) is str:
                config['process']['juphoon'] = config['process']['juphoon'].split()
            if type(config['process']['android']) is str:
                config['process']['android'] = config['process']['android'].split()

            self.process = config['process']['juphoon'] + config['process']['android']
            self.pids = []
        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)

    def getpid(self):
        pfile = glob.glob(self.files['process'])[0]
        #note: use native ps not,busybox ps, sample is listed below
        #system    1681  283   724960 65316 SyS_epoll_ b6d38f54 S com.juphoon.sprd.service
        if pfile:
            with open(pfile) as processfile:
                for line in processfile:
                    for i,pname in enumerate(self.process):
                        if pname in line:
                            pinfo = line.split()
                            print pinfo[8] + ', pid is ' + pinfo[1]
                            self.pids.append(pinfo[1])

    def getflow(self):
        self.getpid()
        log = glob.glob(self.files['log'])[0]
        #index = 0
        if log:
            #get main log's date, 0-main-04-17-23-20-45.log
            timestamp = log[7:].split('.')[0]
            trimlog = timestamp + '_trim.log'
            with open(trimlog, 'w') as tlog:
                tlog.truncate()
            with open(log) as logfile:
                for line in logfile:
                    for i,pid in enumerate(self.pids):
                        if pid in line:
                            #index += 1
                            with open(trimlog, 'a+') as tlog:
                                tlog.write(line)
        #print index

if __name__ == '__main__':
    lp = logParser()
    #lp.testfile()
    lp.getflow()
    print 'done'