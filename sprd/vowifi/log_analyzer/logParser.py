#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com




#TOOD: 1. fix log parse tag bug
#      2. add logic to iterate main log and merge radio.log
#      3. add merge by timeline function





import os
import sys
import glob
from configobj import ConfigObj,ConfigObjError

from lib.logConf import logConf
from lib.utils import utils
import logging

'''
two ways to track logs:
1. by pid, but process may stop, so pid changes
2. by log tags,  but tags can be trivial.
'''


class logParser():

    def __init__(self, logname, filterlevel='low', outputdir= './'):
        try:
            configfile = 'config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.files = dict()
            #self.files['log'] = config['files']['log']
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
            self.words = dict()

            #keywords may be in wrong place, each
            self.priority = dict()

            #prepare the log file handle
            '''
            logList = glob.glob(self.files['log'])[0]
            if not logList:
                print 'no log file found.'
                return
            '''
            self.loglevel =  config['logging']['loglevel']

            #have to set loglevel to interger...
            self.logger = logConf(debuglevel=logging.getLevelName(self.loglevel))

            self.utils = utils(configpath='./')
            realpath = os.path.realpath(logname)
            self.log = realpath
            self.trimlog = outputdir + filterlevel + '_' + os.path.basename(realpath)

            with open(self.trimlog, 'w') as tlog:
                tlog.truncate()#index = 0
            self.processout = outputdir + 'processout.log'

            self.tagfile = "processtags"

            self.defaultoccurnum = 1
            self.lemonoccurnum = 50

        except (ConfigObjError, IOError) as e:
             print('Could not read "%s": %s' % (configfile, e))

    '''
        the function is used to get pid from ps output
    '''
    def getpid(self):
        pfileList = glob.glob(self.files['process'])[0]
        if not pfileList:
            self.logger.logger.error('no process log file found.')
            return
        pfile = pfileList[0]
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
                            self.piddb[lpid] = dict()
                            self.piddb[lpid]['process'] = lprocess
                            self.piddb[lpid]['tags'] = dict()


    def getflow(self, has_ps=True):
        if has_ps:
            self.getpid()
        else:
            self.getPidsByTagsAndWords()
        if self.log:
            #get main log's date, 0-main-04-17-23-20-45.log
            matchindex = 0
            with open(self.log) as logfile:
                for lineno,line in enumerate(logfile):
                    for i,pid in enumerate(self.pids):
                        lineinfo = line.split()
                        #error check
                        if len(lineinfo) < 6:
                            self.logger.logger.info(line)
                            self.logger.logger.info("line " + str(lineno) + " is incorrect")
                            break

                        lpid = lineinfo[2]
                        ltag = lineinfo[5].replace(":", "")

                        if (lpid is None) or (ltag is None):
                            self.logger.logger.error("lpid or ltag is none")
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
                            if self.piddb[pid]['istags']:
                                if ltag not in self.piddb[pid]['tags']:
                                    self.piddb[pid]['tags'][ltag] = 1
                                else:
                                    self.piddb[pid]['tags'][ltag] += 1
        self.logger.logger.info("total " + str(matchindex) + " lines.")
        return self.log


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
        self.logger.logger.info('dump tagsinfo')
        for process, tag in self.tags.iteritems():
            self.logger.logger.info(process)
            self.logger.logger.info(tag)


    def getPidsByTagsAndWords(self):
        #lemon log is not so good
        wordssection = self.config['words']
        for process in wordssection:
            self.words[process] = dict()
            self.words[process]['words'] = wordssection[process]
            self.words[process]['found'] = 0

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
            for tagindex in range(0, taglen):
                tagstr = taginfo[tagindex].split(':')
                #error check
                if len(tagstr) < 2:
                    self.logger.logger.error('taginfo is invalid :' + str(tagstr))
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
                        self.logger.logger.error("line " + str(lineno) + " is incorrect")
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
                                    self.logger.logger.info('lineno is ' + str(lineno)+' foundnum pid for ' + process)
                                    taginfo['foundnum'] += 1
                                    if taginfo['foundnum'] == taginfo['level']: # ok add pid
                                        self.tags[process]['pid'] = lpid
                                        self.tags[process]['found'] = 1

                                        self.pids.append(lpid)
                                        self.piddb[lpid] = dict()
                                        self.piddb[lpid]['process'] = process
                                        self.piddb[lpid]['istags'] = 1
                                        self.piddb[lpid]['tags'] = dict()
                                        self.logger.logger.info('pid ' + str(lpid) + ' is for ' +  process)
                                    break # break from  for i, taginfo in enumerate(tagdes):
                        else:
                            continue # executed if the loop ended normally (no break)
                        break    # executed if 'continue' was skipped (break)

                    #add logic to track service and security
                    for process in wordssection:
                       if int(self.words[process]['found']) == 0 and self.words[process]['words'] in line:
                           self.words[process]['found'] = 1
                           self.words[process]['pid'] = lpid
                           self.pids.append(lpid)
                           self.piddb[lpid] = dict()
                           self.piddb[lpid]['process'] = process
                           self.piddb[lpid]['istags'] = 0


        with open(self.processout, 'w') as processout:
            processout.truncate()
        for process, content in self.tags.iteritems():
            self.logger.logger.info(process)
            self.logger.logger.info(content)

            if 'pid' in content:
                lpid = content['pid']
                self.logger.logger.info(process + ' pid is '+ str(lpid))
                with open(self.processout, 'a+') as processout:
                    linfo = process + ':' + str(lpid) + '\n'
                    processout.write(linfo)

        for process, content in self.words.iteritems():
            self.logger.logger.info(process)
            self.logger.logger.info(content)
            if 'pid' in content:
                lpid = content['pid']
                self.logger.logger.info(process + ' pid is '+ str(lpid))
                with open(self.processout, 'a+') as processout:
                    linfo = process + ':' + str(lpid) + '\n'
                    processout.write(linfo)

    def getTagsNum(self):
        """
        The function is used to get all tags and tags' num from existing ps log
        """
        self.gettags()



if __name__ == '__main__':
    lp = logParser(logname='./0-main-06-07-12-09-45.log', filterlevel='high', outputdir='./')

    lp.getflow(has_ps=False)
    print('done')