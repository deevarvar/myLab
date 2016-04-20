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
            self.config = config
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
            #pid array
            self.pids = []

            #struct to contain 'process'(str), 'tags'(list)
            self.piddb = {}

            self.tags = {}

            #keywords may be in wrong place, each
            self.priority = {}

            #prepare the log file handle
            self.log = glob.glob(self.files['log'])[0]
            timestamp = self.log[7:].split('.')[0]
            self.trimlog = timestamp + '_' + filterlevel + '.log'
            with open(self.trimlog, 'w') as tlog:
                tlog.truncate()#index = 0

            self.tagfile = "processtags"

            self.defaultoccurnum = 1
            self.lemonoccurnum = 50

            with open(self.tagfile, 'w') as ptags:
                ptags.truncate()

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)

    def getpid(self):
        pfile = glob.glob(self.files['process'])[0]
        #note: use native ps, not busybox ps, sample is listed below
        #system    1681  283   724960 65316 SyS_epoll_ b6d38f54 S com.juphoon.sprd.service
        if pfile:
            with open(pfile) as processfile:
                for line in processfile:
                    for i,pname in enumerate(self.process):
                        if pname in line:
                            pinfo = line.split()
                            lprocess = pinfo[8]
                            lpid = pinfo[1]
                            with open(self.trimlog, 'a+') as tlog:
                                tlog.write(lprocess + ' is ' + lpid + '\n')
                            self.pids.append(lpid)
                            self.piddb[lpid] = {}
                            self.piddb[lpid]['process'] = lprocess
                            self.piddb[lpid]['tags'] = []

    def getflow(self):
        self.getpid()
        if self.log:
            #get main log's date, 0-main-04-17-23-20-45.log
            matchindex = 0
            with open(self.log) as logfile:
                for lineno,line in enumerate(logfile):
                    for i,pid in enumerate(self.pids):
                        lineinfo = line.split()
                        #error check
                        if len(lineinfo) < 6:
                            print line
                            print "line " + str(lineno) + " is incorrect"
                            continue

                        lpid = lineinfo[2]
                        ltag = lineinfo[5].replace(":", "")

                        if (lpid is None) or (ltag is None):
                            print "lpid or ltag is none"
                            continue

                        if pid == lpid:
                            matchindex += 1
                            #get the line
                            with open(self.trimlog, 'a+') as tlog:
                                tlog.write(line)
                            #get tags

                            #the two tags are non-sense
                            if ltag == "System.out" or ltag == "System":
                                continue
                            if ltag not in self.piddb[pid]['tags']:
                                self.piddb[pid]['tags'].append(ltag)

        print "total " + str(matchindex) + " lines."

    def gettags(self):
        #just parse the high level's log
        #use dict to store the pid
        self.getflow()
        with open(self.tagfile, "a+") as tfile:
            for i, pid in enumerate(self.pids):
                alltags = ''
                for i,processtag in enumerate(self.piddb[pid]['tags']):
                    alltags = alltags + processtag + " "
                tfile.write(self.piddb[pid]['process'] + "=" + alltags + '\n')

    def writetags(self):
        #FIXME: need to manually remove those tags not needed
        #the logic is here, just need the first tag to identify
        tagssections = {}
        for i, pid in enumerate(self.pids):
            taglist = self.piddb[pid]['tags']
            if taglist:
                lproc = self.piddb[pid]['process']
                firsttag = taglist[0]
                lprio = self.defaultoccurnum
                #special handling, LEMON need more check
                if firsttag == 'LEMON':
                    lprio = self.lemonoccurnum
                tagssections[firsttag] = lproc + ','+ str(lprio)

        self.config['tags'] = tagssections
        self.config.write()


    def getPidsByTags(self):
        #lemon log is not so good

        tagsection = self.config['tags']
        for tag in tagsection:
            self.tags[tag] = {}
            #the whole string...
            taginfo = tagsection[tag].split(',')
            self.tags[tag]['name'] = taginfo[0]
            self.tags[tag]['level'] = int(taginfo[1]) #NOTE convert str to int
            self.tags[tag]['found'] = 0

        if self.log:
            with open(self.log) as logfile:
                for lineno,line in enumerate(logfile):
                    lineinfo = line.split()

                    #for debug to scan only range
                    #if lineno < 4421 or lineno > 4421:
                    #    continue
                    #print lineinfo

                    #error check
                    if len(lineinfo) < 6:
                        print "line " + str(lineno) + " is incorrect"
                        continue

                    ltag = lineinfo[5].replace(":", "")
                    lpid = lineinfo[2]
                    #print ltag + ' '+ str(lpid)
                    #need to add priority to check if found
                    for tag in tagsection:
                        if self.tags[tag]['found'] != self.tags[tag]['level']:
                            #print tag + ' vs ' + ltag
                            if tag == ltag:
                                print 'lineno is ' + str(lineno)+' found pid for ' + self.tags[tag]['name']
                                self.tags[tag]['found'] += 1
                                if self.tags[tag]['found'] == self.tags[tag]['level']:
                                    self.tags[tag]['pid'] = lpid
                                    print 'pid ' + str(lpid) + ' is for ' +  self.tags[tag]['name']
                                break  # break from this line's for tag in tagsection

        for tag, process in self.tags.iteritems():
            print process
            if 'pid' in process:
                print tag + ' ' + process['name'] + ' pid is '+ str(process['pid'])

if __name__ == '__main__':
    lp = logParser(filterlevel='high')

    #just need to run once to update config.ini's tags section
    lp.gettags()
    lp.writetags()

    lp.getPidsByTags()

    print 'done'