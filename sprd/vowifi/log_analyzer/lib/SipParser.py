#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
import sys
import re
from configobj import ConfigObj,ConfigObjError

path = os.path.dirname(os.path.realpath(__file__))


class SipParser():
    def __init__(self, configpath='..'):
        try:
            configfile = configpath + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.reqline = config['sipParser']['reqline']
            self.rspline = config['sipParser']['rspline']
            self.headerline = config['sipParser']['headerline']
            self.cseqline = config['sipParser']['cseqline']

            #define compact headers
            #http://www.cs.columbia.edu/sip/compact.html
            self.sipcompact = dict()
            self.sipcompact['a'] = 'Accept-Contact'
            self.sipcompact['b'] = 'Referred-By'
            self.sipcompact['c'] = 'Content-Type'
            self.sipcompact['e'] = 'Content-Encoding'
            self.sipcompact['f'] = 'From'
            self.sipcompact['i'] = 'Call-ID'
            self.sipcompact['k'] = 'Supported'
            self.sipcompact['l'] = 'Content-Length'
            self.sipcompact['m'] = 'Contact'
            self.sipcompact['o'] = 'Event'
            self.sipcompact['r'] = 'Refer-To'
            self.sipcompact['s'] = 'Subject'
            self.sipcompact['t'] = 'To'
            self.sipcompact['u'] = 'Allow-Events'
            self.sipcompact['v'] = 'Via'


        except (ConfigObjError, IOError) as e:
             print('Could not read "%s": %s' % (configfile, e))

    def getMethod(self, line):
        reqpattern = re.compile(self.reqline)
        match = reqpattern.search(line)
        if not match:
            print 'no req in line ' + line
            return
        method = match.group(1)
        print method
        return method

    def getStatusLine(self, line):
        rsppattern = re.compile(self.rspline)
        match = rsppattern.search(line)
        if not match:
            print 'no rsp in line ' + line
            return
        status = match.group(1)
        print status
        return status

    def getCSeq(self, line):
        cseqpattern = re.compile(self.cseqline)
        match = cseqpattern.search(line)
        if not match:
            print 'no cseq in line ' + line
            return
        cseq = match.group(1)
        print cseq
        return cseq

    def getHeaderline(self, line):
        headerpattern = re.compile(self.headerline)
        match = headerpattern.search(line)
        #print self.headerline, line
        if not match:
            print 'no rsp in line ' + line
            return
        header = match.group(1)
        content = match.group(2)
        pair = dict()
        pair['header'] = header
        pair['content'] = content
        print 'header is ' + pair['header'] + ', content is ' + pair['content']
        return pair

if __name__ == '__main__':
    reqline = "04-17 23:21:27.697  1681  2968 D LEMON   : REGISTER sip:ims.mnc872.mcc405.3gppnetwork.org SIP/2.0"
    sp = SipParser()
    sp.getMethod(reqline)
    rspline = "04-17 23:33:02.798  1681  2968 D LEMON   : SIP/2.0 180 Ringing"
    sp.getStatusLine(rspline)
    headerline = "04-17 23:33:02.798  1681  2968 D LEMON   : Call-ID: CAAF438FE7D8F8B0D054DD5B@1370ffffffff"
    sp.getHeaderline(headerline)
    cseqline = "04-17 23:34:39.275  1681  2968 D LEMON   : CSeq:9 ACK"
    sp.getCSeq(cseqline)
