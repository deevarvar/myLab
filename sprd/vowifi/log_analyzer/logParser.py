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
    def __init__(self, filterlevel='low'):
        try:
            configfile = 'config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.files = {}
            self.files['log'] = config['files']['log']
            self.files['process'] = config['files']['process']

            filterinfo = config['filterlevels'][filterlevel]
            #if only str, convert to list
            if type(filterinfo['juphoon']) is str:
                filterinfo['juphoon'] = filterinfo['juphoon'].split()
            if type(filterinfo['android']) is str:
                filterinfo['android'] = filterinfo['android'].split()

            self.process = filterinfo['juphoon'] + filterinfo['android']
            self.pids = []

            #prepare the log file handle
            self.log = glob.glob(self.files['log'])[0]
            timestamp = self.log[7:].split('.')[0]
            self.trimlog = timestamp + '_' + filterlevel + '.log'
            with open(self.trimlog, 'w') as tlog:
                tlog.truncate()#index = 0

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
                            with open(self.trimlog, 'a+') as tlog:
                                tlog.write(pinfo[8] + ' is ' + pinfo[1] + '\n')
                            self.pids.append(pinfo[1])

    def getflow(self):
        self.getpid()
        if self.log:
            #get main log's date, 0-main-04-17-23-20-45.log
            index = 0
            with open(self.log) as logfile:
                for line in logfile:
                    for i,pid in enumerate(self.pids):
                        if pid in line:
                            index += 1
                            with open(self.trimlog, 'a+') as tlog:
                                tlog.write(line)
        print "total " + str(index) + " lines."

    def gettags(self):
        #just parse the high level's log
        pass

    def getPidsByTags(self):
        pass

if __name__ == '__main__':
    lp = logParser(filterlevel='high')
    #lp.testfile()
    lp.getflow()
    print 'done'