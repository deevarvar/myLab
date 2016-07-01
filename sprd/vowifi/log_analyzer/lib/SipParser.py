#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
import sys
import re
from configobj import ConfigObj,ConfigObjError
from constants import Q850map
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('./')
from logConf import logConf
import logging

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
            self.numpattern = config['sipParser']['numpattern']
            self.ippattern = config['sipParser']['ippattern']
            self.pasopattern = config['sipParser']['pasopattern']
            self.sdppattern = config['sipParser']['sdppattern']
            self.directpattern = config['sipParser']['directpattern']
            self.mediapattern = config['sipParser']['mediapattern']
            self.b2buapattern = config['sipParser']['b2buapattern']
            self.causepattern =  config['sipParser']['causepattern']

            #define compact headers
            #http://www.cs.columbia.edu/sip/compact.html
            self.sipcompact = dict()
            self.sipcompact['Accept-Contact'] = 'a'
            self.sipcompact['Referred-By'] = 'b'
            self.sipcompact['Content-Type'] = 'c'
            self.sipcompact['Content-Encoding'] = 'e'
            self.sipcompact['From'] = 'f'
            self.sipcompact['Call-ID'] = 'i'
            self.sipcompact['Supported'] = 'k'
            self.sipcompact['Content-Length'] = 'l'
            self.sipcompact['Contact'] = 'm'
            self.sipcompact['Event'] = 'o'
            self.sipcompact['Refer-To'] = 'r'
            self.sipcompact['Subject'] = 's'
            self.sipcompact['To'] = 't'
            self.sipcompact['Allow-Events'] = 'u'
            self.sipcompact['Via'] = 'v'

            #singleton logger
            self.logger = logConf()

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)

    def getMethod(self, line):
        reqpattern = re.compile(self.reqline)
        match = reqpattern.search(line)
        if not match:
            self.logger.logger.debug('no req in line ' + line)
            return None
        method = match.group(1).strip()
        self.logger.logger.info('method is ' + method)
        return method

    def getStatusLine(self, line):
        rsppattern = re.compile(self.rspline)
        match = rsppattern.search(line)
        if not match:
            self.logger.logger.debug('no rsp in line ' + line)
            return None
        status = match.group(1).strip()
        self.logger.logger.info('status line is ' + status)
        return status

    def getCSeq(self, line):
        cseqpattern = re.compile(self.cseqline)
        match = cseqpattern.search(line)
        if not match:
            self.logger.logger.debug('no cseq in line ' + line)
            return None
        cseq = match.group(1).strip()
        self.logger.logger.info('CSeq is ' + cseq)
        return cseq

    def checkCompact(self, source, target):
        if source == target or  (target in self.sipcompact and source == self.sipcompact[target]):
            self.logger.logger.info('found header ' + target)
            return True
        else:
            return False

    def getHeaderContent(self,line, headername):
        pair = self.getHeaderline(line)

        if not pair:
            return None

        header = pair['header']
        content = pair['content']
        if self.checkCompact(header, headername):
            return content
        else:
            self.logger.logger.debug('no ' + headername + ' in line ' + line)
            return None


    def getHeaderline(self, line):
        headerpattern = re.compile(self.headerline)
        match = headerpattern.search(line)
        #print self.headerline, line
        if not match:
            self.logger.logger.debug('no rsp in line ' + line)
            return None
        header = match.group(1)
        content = match.group(2)
        pair = dict()
        pair['header'] = header
        pair['content'] = content.strip()
        self.logger.logger.info('header is ' + pair['header'] + ', content is ' + pair['content'])
        return pair

    def getPasoUri(self, line):
        pasopattern = re.compile(self.pasopattern)
        match = pasopattern.search(line)
        if not match:
            return None
        #P-Associate-URI is comma seperated or a list of P-Associate-URI
        #1.P-Associated-URI: <sip:+11234567890@TEST.3GPP.COM>,<tel:+11234567890>
        #2. P-Associated-URI: <sip:+11234567890@TEST.3GPP.COM>
        #   P-Associated-URI: <tel:+11234567890>
        pasouris = match.group(1).strip()
        paso = pasouris.split(',')[0]
        pasonum = self.getNumber(paso)
        self.logger.logger.info('P-Associate-URI is ' + str(pasonum))
        return pasonum

    def getNumber(self, string):
        numpattern = re.compile(self.numpattern)
        match = numpattern.search(string)
        if not match:
            self.logger.logger.debug('no num in string ' + string)
            return None

        num = match.group(2).strip()
        num = num.split('@')[0]
        #print num
        return num

    def checkIp(self, string):
        ippattern = re.compile(self.ippattern)
        match = ippattern.search(string)
        if not match:
            #self.logger.logger.debug('no ip in string ' + string)
            return False
        else:
            ip = match.group(0).strip()
            #self.logger.logger.debug('find ip: ' + ip)
            return True

    def sdpParser(self, line):
        sdppattern = re.compile(self.sdppattern)
        match = sdppattern.search(line)
        if not match:
            return None
        type = match.group(1).strip()
        value = match.group(2).strip()
        pair = dict()
        pair['type'] = type
        pair['value'] = value
        self.logger.logger.info('header is ' + pair['type'] + ', content is ' + pair['value'])
        return pair

    def getmedia(self, value):
        '''
         m=audio 37042 RTP/AVP 104 0 8 116 103 9 101
        :param value: the string after "m="
        :return:
        '''
        mediapattern = re.compile(self.mediapattern)
        match = mediapattern.search(value)
        if not match:
            return None
        pair = dict()
        pair['mtype'] = match.group(1).strip()
        #<port>/<number of ports>
        pair['mport'] = match.group(2).strip().split('/')[0]
        pair['mproto'] = match.group(3).strip()
        pair['mfmt'] = match.group(4).strip()
        self.logger.logger.info('media type is ' + pair['mtype'] + ', port is ' + pair['mport'])
        return pair


    def checksdpDirect(self, line):
        directpattern = re.compile(self.directpattern)
        match = directpattern.search(line)
        if not match:
            return False
        else:
            return True

    def checkB2BUA(self, line):
        b2buapattern = re.compile(self.b2buapattern)
        match = b2buapattern.search(line)
        if not match:
            return False
        else:
            return True

    def getCause(self, line):
        causepattern = re.compile(self.causepattern)

        match = causepattern.search(line)
        if match:
            cause = dict()
            cause['code'] = match.group(1).strip()
            cause['isdn'] = ''
            if str(cause['code']) in Q850map:
                cause['isdn'] = Q850map[cause['code']]['isdn']
            self.logger.logger.info('cause code is ' + str(cause['code']) + ', string is ' + cause['isdn'] )
            return cause
        else:
            return False

if __name__ == '__main__':
    #TODO write own ut function
    reqline = "04-17 23:21:27.697  1681  2968 D LEMON   : REGISTER sip:ims.mnc872.mcc405.3gppnetwork.org SIP/2.0"
    sp = SipParser()
    sp.getMethod(reqline)
    rspline = "04-17 23:33:02.798  1681  2968 D LEMON   : SIP/2.0 180 Ringing"
    sp.getStatusLine(rspline)
    headerline = "04-17 23:33:02.798  1681  2968 D LEMON   : Call-ID: CAAF438FE7D8F8B0D054DD5B@1370ffffffff"
    sp.getHeaderline(headerline)
    cseqline = "04-17 23:34:39.275  1681  2968 D LEMON   : CSeq:9 ACK"
    sp.getCSeq(cseqline)

    callidline1 = "05-05 16:09:30.385  1965  2897 D LEMON   : i:I2bu99501.6v.eopCs2421Cn.i@[2405:204:1a03:45c7::2aa3:38ac]"
    callidline2 = "05-05 16:07:55.412  1965  2897 D LEMON   : Call-ID: I2bu99501.6v.eopCs2421Cn.i@[2405:204:1a03:45c7::2aa3:38ac]"
    sp.getHeaderContent(callidline1, 'Call-ID')
    sp.getHeaderContent(callidline2, 'Call-ID')

    fromline1 = "05-05 16:16:36.286  1965  2897 D LEMON   : From: \"+917011021774\"<sip:+917011021774@ims.mnc872.mcc405.3gppnetwork.org>;tag=chi6.0WU1e0Z4WD9"
    fromline2 = "05-05 16:16:36.195  1965  2897 D LEMON   : f:\"+917011021774\"<sip:+917011021774@ims.mnc872.mcc405.3gppnetwork.org>;tag=chi6.0WU1e0Z4WD9"
    sp.getHeaderContent(fromline1, 'From')
    sp.getHeaderContent(fromline2, 'From')

    fromtag = "from:<sip:+917011021754@ims.mnc872.mcc405.3gppnetwork.org>;tag=atqPR_w.eSVudV4213iBTI1a_7"
    totag = "to:\"+917011021774\"<sip:+917011021774@ims.mnc872.mcc405.3gppnetwork.org>;tag=chi6.0WU1e0Z4WD9"
    fromteltag = "f:<tel:+917011021790>;tag=7B_g338Ve240ZYaA"
    smstotag = "To:<sip:10.56.4.26>"
    fromnum = sp.getNumber(fromtag)
    tonum = sp.getNumber(totag)
    fromtel = sp.getNumber(fromteltag)
    smsto = sp.getNumber(smstotag)
    print fromnum, tonum, fromtel, smsto

    ip = sp.checkIp(smstotag)
    print ip

    pasotag = "P-Associated-URI: <sip:+11234567890@TEST.3GPP.COM>,<tel:+11234567890>"
    paso = sp.getPasoUri(pasotag)
    print paso

    sdptag1 = "03-18 18:47:48.263  2617  3010 D LEMON   : m=audio 37042 RTP/AVP 104 0 8 116 103 9 101"
    sdptag2 = "03-18 18:47:48.263  2617  3010 D LEMON   : v=0"
    mtag = sp.sdpParser(sdptag1)
    sp.getmedia(mtag['value'])
    sp.sdpParser(sdptag2)

    print sp.checksdpDirect('recvonl')
    print sp.checksdpDirect('inactive')

    b2btag = "06-07 12:21:20.705  1948  3081 D LEMON   : P-Com.Nokia.B2BUA-Involved:no"
    print sp.checkB2BUA(b2btag)

    causetag ="06-23 13:31:18.635  2140  6550 D LEMON   : Reason:Q.850;cause=16"
    cause = sp.getCause(causetag)
    print cause['code']