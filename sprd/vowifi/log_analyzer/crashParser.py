#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com


import os
import re

path = os.path.dirname(os.path.realpath(__file__))
from configobj import ConfigObj,ConfigObjError
#import actionBuilder
from radioParser import *

class crashParser():
    def __init__(self, logname):
        configfile = path + '/config.ini'
        self.utils = utils()
        try:
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.log = os.path.realpath(logname)
            self.crashpattern = dict()
            self.crashpattern['app'] = "E AndroidRuntime: Process:"
            self.crashpattern['native'] = ">>>.*<<<"
            #app crash: 04-13 19:57:30.414  6461  6461 E AndroidRuntime: Process: com.spreadtrum.vowifi, PID: 6461
            #native crash: 01-04 04:24:23.131  5246  5246 F DEBUG   : pid: 1252, tid: 5034, name: Binder:1252_3  >>> com.spreadtrum.vowifi <<<
            self.loglines = list()
            self.crashmsgs = list()
            self.logger = logConf()

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)

    def initcrashmsg(self, line):
        crashmsg = dict()
        fields = line.strip().split(' ')
        #04-17 23:21:24.420
        #fix android O parsing
        fruit = self.utils.findfields(fields)
        timestamp = fruit['day'] + ' ' + fruit['time']
        crashmsg['timestamp'] = timestamp
        crashmsg['issip'] = 0
        crashmsg['iscrash'] = 1
        '''
        crashmsg['action'] should be a dict
        member should be eventname, color, msglevel
        '''
        crashmsg['action'] = ''
        crashmsg['report'] = None
        crashmsg['line'] = line
        crashmsg['lineno'] = None
        #AP -> UE
        crashmsg['direct'] = '->'
        return crashmsg

    def parsenativecrash(self, line):
        #native crash: 01-04 04:24:23.131  5246  5246 F DEBUG   : pid: 1252, tid: 5034, name: Binder:1252_3  >>> com.spreadtrum.vowifi <<<
        crashmsg = self.initcrashmsg(line)
        npattern = re.compile(r'' + "pid:(.*),.*>>>(.*)<<<")
        match = npattern.search(line)
        if match and len(match.groups()) == 2:
            pid = str(match.group(1)).strip()
            process = str(match.group(2)).strip()
            #set eventname
            eventname = process + ' Crashed!' + '\n' + "Pid:" + pid
            color = 'red'
            msglevel = Msglevel.ERROR
            action = actionBuilder()
            action.setAll(eventname, msglevel, color)
            crashmsg['action'] = action
            #set report
            event = process + ' Crashed!'
            crashmsg['report'] = constructReport(type=ReportType.PHONEEVENT_BASE, event=event, level=msglevel)

            self.crashmsgs.append(crashmsg)

    def parseappcrash(self, line):
        #app crash: 04-13 19:57:30.414  6461  6461 E AndroidRuntime: Process: com.spreadtrum.vowifi, PID: 6461
        crashmsg = self.initcrashmsg(line)
        apattern =  re.compile(r'' + "Process:(.*), PID:(.*)")
        match = apattern.search(line)
        if match and len(match.groups()) == 2:
            pid = str(match.group(2)).strip()
            process = str(match.group(1)).strip()
            #set eventname
            eventname = process + ' Crashed!' + '\n' + "Pid:" + pid
            color = 'red'
            msglevel = Msglevel.ERROR
            action = actionBuilder()
            action.setAll(eventname, msglevel, color)
            crashmsg['action'] = action
            #set report
            event = process + ' Crashed!'
            crashmsg['report'] = constructReport(type=ReportType.PHONEEVENT_BASE, event=event, level=msglevel)
            self.crashmsgs.append(crashmsg)

    def parselog(self):

        if os.path.isfile(self.log) is False:
            return None

        with open(self.log, 'rb') as logfile:
            self.loglines = logfile.readlines()

        for i,line in enumerate(self.loglines):
            apppattern = re.compile(self.crashpattern['app'])
            nativepattern = re.compile(self.crashpattern['native'])
            match = apppattern.search(line)
            if match:
                self.parseappcrash(line)
                continue

            match = nativepattern.search(line)
            if match:
                self.parsenativecrash(line)

        #add debug logs

        for index, cmsg in enumerate(self.crashmsgs):
            self.logger.logger.info('request index is ' + str(index))
            for key,value in cmsg.iteritems():
                self.logger.logger.info(str(key) + ':' + str(value))

    def getmsgs(self):
        return self.crashmsgs


if __name__ == '__main__':
#crash sample:
#1. native crash: D:\code\so\juphoonlib\develop\7lib\sos\5
#2. app crash:    D:\code\merge\dtac\call_crash\android
#native crash/app crash , two category
    appcp = crashParser('./appcrash.log')
    appcp.parselog()
    nativecp = crashParser('./nativecrash.log')
    nativecp.parselog()