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
    def __init__(self):
        try:
            configfile = 'config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.files = dict()
            self.files['log'] =  config['samsung']['log']
            self.keywords = dict()
            self.keywords['recv'] = config['samsung']['recv']
            self.keywords['sendreq'] = config['samsung']['sendreq']
            self.keywords['sendrsp'] = config['samsung']['sendrsp']

        except (ConfigObjError, IOError) as e:
             print('Could not read "%s": %s' % (configfile, e))

    def getflow(self):
        #hard code here
        samsungfileList = glob.glob(self.files['log'])
        if not samsungfileList:
            print 'no samsung log file found.'
            return
        samsungfile = samsungfileList[0]
        self.trimlog = 'trim_' + samsungfile
        with open(self.trimlog, 'w') as tlog:
            tlog.truncate()

        with open(samsungfile) as sfile:
            for line in sfile:
                rePattern = r'' + self.keywords['recv'] + '|' + self.keywords['sendreq'] + '|' + self.keywords['sendrsp']
                samsungPattern = re.compile(rePattern)
                if samsungPattern.search(line):
                    with open(self.trimlog, 'a+') as tlog:
                        tlog.write(line)


if __name__ == '__main__':
    print 'start to parse samsung'
    sp = samsungParser()
    sp.getflow()