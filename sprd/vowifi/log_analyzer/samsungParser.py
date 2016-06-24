# -*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
import sys
import glob
from configobj import ConfigObj,ConfigObjError
import re


'''
1. recv : SipStackTransportCallback.*Cseq
2. send req : SipStackBuildFinalReq:SIP Message
3. send rsp : SipStackTransportSendRsp:SIP RSP Message
'''

class samsungParser():
    def __init__(self,logname):
        try:
            configfile = 'config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.files = dict()
            self.files['log'] =  config['samsung']['log']
            self.keywords = dict()
            self.keywords['recv'] = config['samsung']['keywords']['recv']
            self.keywords['sendreq'] = config['samsung']['keywords']['sendreq']
            self.keywords['sendrsp'] = config['samsung']['keywords']['sendrsp']
            self.keywords['ikemsg'] = config['samsung']['keywords']['ikemsg']

            realpath = os.path.realpath(logname)
            self.file = realpath

        except (ConfigObjError, IOError) as e:
             print('Could not read "%s": %s' % (configfile, e))

    def getflow(self):
        #hard code here
        '''
        samsungfileList = glob.glob(self.files['log'])
        if not samsungfileList:
            print 'no samsung log file found.'
            return
        '''

        samsungfile = self.file
        basename = os.path.basename(samsungfile)
        trimname = 'trim_' + basename
        self.trimlog = os.path.dirname(samsungfile) + '/'+ trimname
        with open(self.trimlog, 'w') as tlog:
            tlog.truncate()
        print self.keywords['ikemsg']
        rePattern = r'' + self.keywords['recv'] + '|' + self.keywords['sendreq'] + '|' + self.keywords['sendrsp'] \
                    + '|' + self.keywords['ikemsg']
        samsungPattern = re.compile(rePattern)
        print "all output will be redirected to " + self.trimlog
        with open(samsungfile) as sfile:
            for lineno, line in enumerate(sfile):
                if samsungPattern.search(line):
                    with open(self.trimlog, 'a+') as tlog:
                        tlog.write(str(lineno) + ' ' + line)


if __name__ == '__main__':
    print 'start to parse samsung'
    sp = samsungParser(logname='./samsung.log')
    sp.getflow()