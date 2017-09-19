#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import sys
import os
#sys.path.append('./')
#print sys.path
import definition
from config import *
from lib.logConf import logConf
from lib.logutils import logutils
from helper.processmap import *
import re

#TODO list:
#1. find pid by words
#1.1 pid may change, process restart
#2. unittest
#3. decode flow
#3.1 idea is different from old style:
#     media only need the process, simple is beautiful.
#     record start
#     record statistics, pps, sps,rtp
#     record end
# for phrase one:
#      1. log grep
#      2. data statistics
#


class mflow:
    def __init__(self, logname='', outdir='./', loglevel='DEBUG'):
        self.log = os.path.realpath(logname)
        with open(self.log, 'rb') as logfile:
            self.loglines = logfile.readlines()
        self.logger = logConf(debuglevel=loglevel)
        self.logger.logger.info('init flow')
        self.config = config()
        self.logutils = logutils()

        #output is in one extra dir
        self.outdir = os.path.dirname(logname) + '/output'
        self.logutils.mkdirp(self.outdir)

        self.trimlog = self.outdir + '/' + 'media_verbose.log'
        with open(self.trimlog, 'a+')as trimlog:
            trimlog.truncate()

        #final eventmsg should be processed
        self.eventmsgs = list()

        #pid should be a verbose list
        self.pids = list()

        #call list
        self.calllist = list()

        #call number
        self.callnum = 0

        #Do we really need this F*cking global flag
        self.incall = False
        self.curcall = None

    def findPid(self):
        '''
        description: process may restart, so pid is a list
        :return:
        '''
        for index, line in enumerate(self.loglines):
            fields = line.split()
            fruit = self.logutils.findfields(fields)
            pid = fruit['pid']
            #start to find pid
            for index, process in enumerate(ProcessList):
                key = process.getkey()
                name = process.getname()
                plist = process.getpidlist()
                if pid not in self.pids and self.logutils.patterninline(key, line):
                    self.logger.logger.info('found id ' + str(pid) + ' for ' + name)
                    self.pids.append(pid)
                    plist.append(pid)


    def parse(self):
        '''
        1. pass pid lines
        2. pattern match
        3. pattern handler
        4. draw the graph, csv,
        :return:
        '''
        #find all pids
        self.findPid()

        #handle each patten by pid
        for index, line in enumerate(self.loglines):
            fields = line.split()
            fruit = self.logutils.findfields(fields)
            pid = fruit['pid']
            for index, process in enumerate(ProcessList):
                plist = process.getpidlist()
                pevent = process.getpevent()
                if pid in plist:
                    #then we handle the event
                    elist = pevent.geteventlist()
                    for eindex, event in enumerate(elist):
                        key = event['key']
                        groupnum = event['groupnum']
                        color = event['color']
                        eventHandler = event['eventHandler']

                        regex = re.compile(key)
                        result = regex.search(line)
                        if result:
                            #redirect output
                            with open(self.trimlog, 'a+') as trimlog:
                                trimlog.write(line)

                            #start to handle event, pass the mflow instance
                            handlerobj = eventHandler(result, color, groupnum, mflow=self, fruit=fruit)
                            eventdict = handlerobj.getret()

    def dumpcalllist(self):
        self.logger.logger.info('Totally Call number is ' + str(self.callnum))
        for cindex, call in enumerate(self.calllist):
            call.dumpcall()

    def exportexcel(self):
        # generate sheet named by VT_Call_number_sendstat/recvstat
        for cindex, call in enumerate(self.calllist):
            pass

if __name__ == '__main__':
    mflow = mflow(logname="./samplelog/main.log")
    mflow.parse()
    mflow.dumpcalllist()
    pass
