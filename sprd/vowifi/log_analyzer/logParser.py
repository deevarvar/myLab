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
            self.files = dict()
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
            self.pids = list()

            #struct to contain 'process'(str), 'tags'(list)
            self.piddb = dict()

            self.tags = dict()

            #keywords may be in wrong place, each
            self.priority = dict()

            #prepare the log file handle
            self.log = glob.glob(self.files['log'])[0]
            timestamp = self.log[7:].split('.')[0]
            self.trimlog = timestamp + '_' + filterlevel + '.log'

            self.processout = 'processout.log'

            self.tagfile = "processtags"

            self.defaultoccurnum = 1
            self.lemonoccurnum = 50

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)

    '''
        the function is used to get pid from ps output
    '''
    def getpid(self):
        pfile = glob.glob(self.files['process'])[0]
        #note: use native ps, not busybox ps, sample is listed below
        #system    1681  283   724960 65316 SyS_epoll_ b6d38f54 S com.juphoon.sprd.service
        if pfile:
            with open(self.trimlog, 'w') as tlog:
                tlog.truncate()#index = 0
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
                            self.piddb[lpid] = dict()
                            self.piddb[lpid]['process'] = lprocess
                            self.piddb[lpid]['tags'] = dict()


    def getflow(self, has_ps=True):
        if has_ps:
            self.getpid()
        else:
            self.getPidsByTags()
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
                            break

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

                            #the two tags make no sense
                            if ltag == "System.out" or ltag == "System":
                                continue
                            if ltag not in self.piddb[pid]['tags']:
                                self.piddb[pid]['tags'][ltag] = 1
                            else:
                                self.piddb[pid]['tags'][ltag] += 1

        print "total " + str(matchindex) + " lines."

    def gettags(self):
        #just parse the high level's log
        #use dict to store the pid
        self.getflow(has_ps=True)

        with open(self.tagfile, 'w') as ptags:
            ptags.truncate()

        with open(self.tagfile, "a+") as tfile:
            for i, pid in enumerate(self.pids):
                alltags = ''
                #here sort tags by occornums
                ltagdict = self.piddb[pid]['tags']
                sortedtags = sorted(ltagdict.items(), key=lambda x:x[1], reverse=True)
                for i,element in enumerate(sortedtags):
                    lprocesstag = element[0]
                    lnum = element[1]
                    alltags = alltags + lprocesstag + ":"+str(lnum) + " "
                tfile.write(self.piddb[pid]['process'] + "=" + alltags + '\n')


    def writetags(self):
        """
        this function is not used any more!
        """
        #FIXME: need to manually remove those tags not needed
        #the logic is here, just need the first tag to identify
        tagssections = dict()
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

    def dumptags(self):
        print 'dump tagsinfo'
        for process, tag in self.tags.iteritems():
            print process
            print tag

    def getPidsByTags(self):
        #lemon log is not so good

        tagsection = self.config['tags']
        for process in tagsection:
            self.tags[process] = dict()
            self.tags[process]['tags'] = list()
            self.tags[process]['found'] = 0

            #the whole string...
            taginfo = tagsection[process].split()
            taglen = len(taginfo)
            
            #tags can be multiple
            ##processname = tag1:num1 tag2:num2
            if taglen == 0:
                continue
            for tagindex in xrange(0, taglen):
                tagstr = taginfo[tagindex].split(':')
                #error check
                if len(tagstr) < 2:
                    print 'taginfo is invalid :' + str(tagstr)
                    continue
                ltagelement = dict()
                ltagelement['name'] = tagstr[0]
                ltagelement['level'] = int(tagstr[1]) #ought to occur times
                ltagelement['foundnum'] = 0
                self.tags[process]['tags'].append(ltagelement)

        #add function dump the tags status
        #self.dumptags()

        if self.log:
            with open(self.log) as logfile:
                for lineno,line in enumerate(logfile):
                    lineinfo = line.split()

                    #for debug to scan only range
                    #if lineno < 3310 or lineno > 3315:
                    #    continue
                    #print lineinfo

                    #error check
                    if len(lineinfo) < 6:
                        print "line " + str(lineno) + " is incorrect"
                        continue

                    ltag = lineinfo[5].replace(":", "")
                    lpid = lineinfo[2]
                    #print ltag + ' '+ str(lpid)
                    #need to add priority to check if foundnumnum
                    for process in tagsection:
                        #print process
                        tagdes = self.tags[process]['tags']  #list tag1:num1 tag2:num2
                        foundflag = self.tags[process]['found']
                        for i, taginfo in enumerate(tagdes):
                            if taginfo['name'] == ltag: #find tag
                                # if already found and check if occurnum ok
                                if  foundflag != 1 and (taginfo['foundnum'] != taginfo['level']):
                                    print 'lineno is ' + str(lineno)+' foundnum pid for ' + process
                                    taginfo['foundnum'] += 1
                                    if taginfo['foundnum'] == taginfo['level']: # ok add pid
                                        self.tags[process]['pid'] = lpid
                                        self.tags[process]['found'] = 1

                                        self.pids.append(lpid)
                                        self.piddb[lpid] = dict()
                                        self.piddb[lpid]['process'] = process
                                        self.piddb[lpid]['tags'] = dict()
                                        print 'pid ' + str(lpid) + ' is for ' +  process
                                    break # break from  for i, taginfo in enumerate(tagdes):
                        else:
                            continue # executed if the loop ended normally (no break)
                        break    # executed if 'continue' was skipped (break)

        with open(self.processout, 'w') as processout:
            processout.truncate()
        for process, content in self.tags.iteritems():
            print process
            print content

            if 'pid' in content:
                lpid = content['pid']
                print process + ' pid is '+ str(lpid)
                with open(self.processout, 'a+') as processout:
                    linfo = process + ':' + str(lpid) + '\n'
                    processout.write(linfo)


    def getTagsNum(self):
        """
        The function is used to get all tags and tags' num from existing ps log
        """
        self.gettags()



if __name__ == '__main__':
    lp = logParser(filterlevel='high')

    lp.getflow(has_ps=False)
    print 'done'