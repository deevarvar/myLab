#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com




#TOOD: 1. fix log parse tag bug
#      2. add logic to iterate main log and merge radio.log
#      3. add merge by timeline function

#TODO:
#     1. genearte a basic error log






import os
import sys
import glob
from configobj import ConfigObj,ConfigObjError
import re
from lib.logConf import logConf
from lib.utils import utils
from seqdiag import parser, builder, drawer
from lib.errormsg import *

import logging

'''
two ways to track logs:
1. by pid, but process may stop, so pid changes
2. by log tags,  but tags can be trivial.
'''


#TODO
#1.  some key words of error log
#2.  error log pattern
#3. service/adpater/imscm flow

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

            self.keywords = config['keywords']['keywords']
            self.utils = utils(configpath='./')

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
            self.trimlog = outputdir + '/logs/'+filterlevel + '_' + os.path.basename(realpath)

            with open(self.trimlog, 'w') as tlog:
                tlog.truncate()#index = 0

            self.processout = outputdir + '/logs/' + 'processout.log'

            self.keylog = outputdir + '/logs/' + 'key_' + os.path.basename(realpath)
            self.elog = outputdir + '/logs/' + 'error_' + os.path.basename(realpath)
            self.diagdir = outputdir + '/diagrams/'

            self.diagstr = ''

            #read errorpattern and keys
            self.errorpattern = dict()
            self.keys = dict()
            self.errorpattern['lemon'] = lemonmsg.errorpattern
            self.errorpattern['imscm'] = imscmmsg.errorpattern
            self.errorpattern['adapter'] = adaptermsg.errorpattern
            self.errorpattern['service'] = servicemsg.errorpattern

            self.keys = dict()
            self.keys['imscmkey'] = self.utils.getPattern(imscmmsg.keys)
            self.logger.logger.error('imscmkey is ' + self.keys['imscmkey'])
            self.keys['adapterkey'] = self.utils.getPattern(adaptermsg.keys)
            self.logger.logger.error('adapterkey is ' + self.keys['adapterkey'] )
            self.keys['lemonkey'] = self.utils.getPattern(lemonmsg.keys)
            self.logger.logger.error('lemonkey is ' + self.keys['lemonkey'])
            self.keys['servicekey'] = self.utils.getPattern(servicemsg.keys)
            self.logger.logger.error('servicekey is ' + self.keys['servicekey'])
            self.keys['s2bkey'] = self.utils.getPattern(s2bmsg.keys)
            self.logger.logger.error('s2bkey is ' + self.keys['s2bkey'])




            with open(self.keylog, 'w') as klog:
                klog.truncate()#index = 0

            with open(self.elog, 'w') as elog:
                elog.truncate()#index = 0

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


    def geterrorlog(self, lineno, line):
        '''
        analyze the line, if meets below:
        1. error msg of all components
        2. key words of all components
        :param lineno:
        :param line:
        :return:
        '''
        allerrorpattern = r'' + self.errorpattern['lemon']  + '|' + \
                          self.errorpattern['adapter'] + '|' + self.errorpattern['service']
        if self.errorpattern['imscm']:
            allerrorpattern += '|' + self.errorpattern['imscm']
        #self.logger.logger.error('allerrorpattern is ' + allerrorpattern);
        repattern = re.compile(allerrorpattern)
        if repattern.search(line):
            with open(self.elog, 'a+') as elog:
                elog.write(str(lineno) + ' ' + line)
            #just copy log to
            with open(self.keylog, 'a+') as klog:
                klog.write(str(lineno) + ' ' + line)


    #get key words log

    def getkeylog(self, lineno, line):

        allkey = self.keys['imscmkey'] + '|' + self.keys['adapterkey'] + '|' + self.keys['lemonkey'] + '|' + self.keys['servicekey'] +'|' + self.keys['s2bkey']

        allkeypattern = re.compile(allkey)
        if allkeypattern.search(line):
            with open(self.keylog, 'a+') as klog:
                klog.write(str(lineno) + ' ' + line)

    def genflowdiag(self):
        #generate the flow diag from the key log
        with open(self.keylog, 'r') as klog:
            for lineno, line in enumerate(klog):
                #iterate the diagkeys
                owner = imscmmsg.owner
                for index, imsdiagkey in enumerate(imscmmsg.diagkeys):
                    key = imsdiagkey['key']
                    role = imsdiagkey['role']
                    action = imsdiagkey['action']
                    keypattern = re.compile(key)
                    if keypattern.search(line):
                        #check role and action:
                        if action == direct_send:
                            direct = ' -> '
                        else:
                            direct = ' <- '
                        chartoremove = ['\"', '\'', '[', ']']
                        line = line.translate(None, ''.join(chartoremove))
                        self.diagstr += role + direct + owner + ' [ label = \"' + line + '\"];\n'

    #FIXME: should put this function into utils.py..., the third function
    def drawDiag(self):
        diagram_definition = u"""seqdiag {\n"""
        #Set fontsize.
        diagram_definition += "default_fontsize = 16;\n"
        #Do not show activity line
        diagram_definition += "activation = none;\n"
        #Numbering edges automaticaly
        diagram_definition +="autonumber = True;\n"
        diagram_definition += self.diagstr
        diagram_definition += u""" }\n"""
        # generate the diag string and draw it
        self.logger.logger.info('seqdiag is ' + diagram_definition)
        #write the diagram string to file
        basename = os.path.basename(self.keylog)
        pngname = basename.split('.')[0] + '.png'
        diagname = basename.split('.')[0] + '.diag'
        pngname = self.diagdir + pngname
        diagname = self.diagdir + diagname
        with open(diagname, 'w') as diagfile:
            diagfile.write(diagram_definition)

        self.utils.setup_imagedraw()
        self.utils.setup_noderenderers()
        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)

        self.logger.logger.info('diagram file is ' + pngname)
        draw = drawer.DiagramDraw('PNG', diagram, filename=pngname, debug=True)
        draw.draw()
        draw.save()



    def getflow(self, has_ps=True):
        if has_ps:
            self.getpid()
        else:
            self.getPidsByTagsAndWords()
        if self.log:
            #get main log's date, 0-main-04-17-23-20-45.log
            matchindex = 0

            with open(self.log, 'rb') as logfile:
                for lineno,line in enumerate(logfile):
                    line = line.strip(' \t')
                    #try to get key log
                    self.geterrorlog(lineno, line)
                    self.getkeylog(lineno,line)

                    allkeywords= self.utils.getPattern(self.keywords)
                    #self.logger.logger.info('allkeywords is ' + allkeywords)
                    if not allkeywords:
                        self.logger.logger.error('allkeywords is none!')
                    else:
                        keyspattern = re.compile(allkeywords)
                        if keyspattern.search(line):
                           with open(self.trimlog, 'a+') as tlog:
                                tlog.write(str(lineno) + ' ' + line)

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
                                tlog.write(str(lineno) + ' ' + line)
                            #get tags

                            #the two tags make no sense
                            if ltag == "System.out" or ltag == "System":
                                continue
                            if self.piddb[pid]['istags']:
                                if ltag not in self.piddb[pid]['tags']:
                                    self.piddb[pid]['tags'][ltag] = 1
                                else:
                                    self.piddb[pid]['tags'][ltag] += 1

                self.genflowdiag()
                self.drawDiag()
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
            with open(self.log, 'rb') as logfile:
                for lineno,line in enumerate(logfile):
                    line = line.strip(' \t')
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
                    #self.logger.logger.error('ltag is ' +ltag)
                    lpid = lineinfo[2]
                    #print ltag + ' '+ str(lpid)
                    #need to add priority to check if foundnumnum
                    for process in tagsection:
                        #in case that do not track some process
                        if process not in self.process:
                            continue
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

                if process == 'com.sprd.ImsConnectionManager' and not lpid:
                    self.errorpattern['imscm'] = str(lpid) + ' .* E '

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
    lp = logParser(logname='./0-main-06-23-13-20-22.log', filterlevel='high', outputdir='./')

    lp.getflow(has_ps=False)
    print('done')