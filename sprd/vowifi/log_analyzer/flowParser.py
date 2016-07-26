#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

'''
#retransmit only covers udp transport
simplify the process:
1. fsm(
2. [TIMER
3. recv.*data
4. process request
5. process response

#error
1. sendto error

TODO:
1. seqdiag DONE

2. dig into sip message
#  2.1 record every request/response
#  2.2 record each field in req/resp
#  2.3 prepare the field parser
#  2.4 store all import field into array and then parse all UE.
#     record INVITE's call-id
#     FIXME: add more logic to check like CSeq and call-id
#     for B2BUA, there is a segment : P-Com.Nokia.B2BUA-Involved:no
#     for following 100 Trying and 200OK , we consider it as B2BUA
#  2.5 add sdp nego logic
#       use cseq and callid, record sdp offer answer, previous action
#  2.6 retransmit/ color:  do retransmit analysis, add record
    # TODO: two dimension:  direct: send/recv;   method: register, invite, ack, 200
    #just loop to find retransmit:  direct, method, cseq
    # show retransmit request no.
#  2.6.1 add reason parsing. - done
#  2.7 add text summary log, running time estimate(sip msg)
#  2.8 add diag for service,adapter, imscm, lemon's fsm
#  2.9 add nortpreceived indication




1. attach
ImsCMUtils: switch to Vowifi
IKE flow
SecurityS2bCallback: mtcS2bCbSuccessed
SecurityS2bWrapper: {"security_json_action":"security_json_action_s2b_successed","security_json_param_local_ip4":"100.80.131.52","security_json_param_local_ip6":"2405:204:1801:c8c5::160a:70b0","security_json_param_pcscf_ip4":"10.56.5.85;10.56.5.70;","security_json_param_dns_ip6":"2405:200:800::1;"}
VoWiFiSecurityS2bWrapper:
RegisterService: INFO: Mtc_CliLogin 1 imsi is 405872000010353, imei is 867400020503813
ImsService: EVENT_WIFI_ATTACH_SUCCESSED-> mFeatureSwitchRequest:ImsServiceRequest->mRequestId:0 mEventCode:100 mServiceId:1
2. register
MTC: INFO: CliLogin with type 256 ip 100.80.131.52
endpoint process [USER REGISTER]
core process event [CIM REQ]. : EN_SIP_SESSE_CIM_REQ
INFO: dlg @10004 process event [CIM REQ].
INFO: dlg @10004 process request <REGISTER>.
dlg @10004 notify event [SEND NONINVITE].
INFO: trans @10006 process request <REGISTER>.
data content[text]: start to print reg , ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ as delimeter
LEMON   : 23:21:22.417 UTPT: INFO: conn[0x3] send data[1750] to [10.56.5.85:5060] ok.
SIP: INFO: core timer process trans event tmr<0xC> [TIMER E].
LEMON   : 23:21:25.019 UTPT: INFO: recv udp data(len:1251) from [10.56.5.85:5060].
trans @10006 process response <REGISTER:401>.
dlg @10004 process response <REGISTER:401>.
core report event [CIM CNF].
LEMON   : 23:21:25.031 RegisterServiceCallback: INFO: mtcCliCbAuthInd, iAutoType: 2, iRegId: 17, pcNonce: gw8zkQAAAABMcdM0AAAAANZmg7pwKwAAP2mHzBVq2sVkNDE0MGQwYw==
LEMON   : 23:21:25.117 RegisterServiceCallback: INFO: mtcCliCbAuthInd, res: f24e745b57c42f32, ck: 26cd44442853d00590f4d4c442519fb4, ik: 0a77aa20b4d76486bb0291eda52a98e1, auts: null
MRF: INFO: endpoint process [USER ENTER PWD].
ZIpsecPfkeyCmdSaAdd
ZIpsecPfkeyCmdSpAdd
INFO: dlg @10005 process event [CIM REQ].
INFO: fsm(MRF_REG) reg@[17] state <REGING> run [USER ENTER PWD] event ok.
send reg again
UTPT: INFO: recv udp data(len:895) from [10.56.5.85:32920].
 trans @10007 process response <REGISTER:200>.
  trans @10007 report event [RECV 2XX].
 dlg @10005 process response <REGISTER:200>.
RegisterServiceCallback: INFO: mtcCliCbRegOk
 VoWifiRegisterManager: callback{"callback_key":"callback_value_login_ok"}
 ImsService: EVENT_WIFI_REGISTER_RESAULT -> result:true, mFeatureSwitchRequest:ImsServiceRequest->mRequestId:0 mEventCode:100 mServiceId:1
subscribe: notify
3. call
3.1 receive call
LEMON   : 23:33:01.359 UTPT: INFO: recv udp data(len:2095) from [10.56.5.85:32920].
fsm(MTF_CALL)
3.2 make call
misc:
zos_dbuf.c 3188 , print the sip msg
pattern: process [
'''

import os
import sys
import glob
import re
from configobj import ConfigObj,ConfigObjError
from seqdiag import parser, builder, drawer
from blockdiag.utils.bootstrap import create_fontmap
from time import gmtime, strftime
import logging
from datetime import datetime
import subprocess
import platform
from PyPDF2 import PdfFileMerger, PdfFileReader

#add user defined lib
#sys.path.append('./lib')
from lib.SipParser import SipParser
from lib.IkeParser import IkeParser
from lib.logConf import logConf
from lib.utils import utils

from lib.constants import *

from logParser import logParser

path = os.path.dirname(os.path.realpath(__file__))



class flowParser():
    def __init__(self, logname):

        try:

            #self.timestamp = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
            #self.logpath = './' + str(self.timestamp) + '.log'

            configfile = path + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.lemontags = config['sprd']['lemontags']
            self.servicetags = config['sprd']['servicetags']
            self.adaptertags = config['sprd']['adaptertags']
            self.sendertags = config['sprd']['sendertags']
            self.receivertags =  config['sprd']['receivertags']
            self.iketags = config['sprd']['iketags'] + '|' + config['sprd']['ikenewtags']
            self.siptags = config['sprd']['siptags']

            #we will split the msg into different pdfs
            self.splitgate = config['utils']['splitgate']

            self.datalentags = config['sprd']['datalentags']
            self.loglevel =  config['logging']['loglevel']


            #list all elements in the scenario
            self.elements = list()

            #a list to split the diagstr
            self.diagstrList = None
            self.pdfList = list()
            #have to set loglevel to interger...
            self.logger = logConf(debuglevel=logging.getLevelName(self.loglevel))
            self.sipparser = SipParser(configpath='./')
            self.ikeParser = IkeParser(configpath='./')
            self.files = dict()
            #despreated logic
           # self.files['log'] = config['files']['log']
            #self.logger.logger.debug('log file pattern is ' +  self.files['log'])



            self.utils = utils(configpath='./')
            realpath = os.path.realpath(logname)
            self.log = realpath
            #/mnt/hgfs/code/github/myLab/sprd/vowifi/log_analyzer/lib/src/3/0-main-3.log, get prefix as dir
            shortname = os.path.basename(realpath)
            dirname = os.path.dirname(realpath)

            prefix = dirname + '/' + shortname.split('.')[0]

            #create the dir tree
            self.utils.createdirs(prefix)
            self.logger.logger.info('start to parse log file: ' + realpath)

            #FIXME: hard coded result log dir
            #defined in config.ini's [utils]->dirnames
            self.resultdir = prefix + '/'
            self.logdir = prefix + '/logs/'

            self.diagdir = prefix + '/diagrams/'
            #for diagrams , we have subdirs diag, pdf
            self.diagdirdiag = prefix + '/diagrams/diag/'
            self.diagdirpdf = prefix + '/diagrams/pdf/'

            self.htmldir = prefix + '/html/'
            self.miscdir = prefix + '/misc/'



            basename = os.path.basename(realpath)
            lemonbasename = 'lemon_' + basename
            self.lemonlog = self.logdir + lemonbasename
            self.keylogall = ''
            self.keylogdaps = ''

            #first we just cache all lines
            with open(self.log, 'rb') as logfile:
                self.loglines = logfile.readlines()

            with open(self.lemonlog, 'w') as tlog:
                tlog.truncate()

            #important structure: sipmsgs, is a list with order
            #currently sipmsgs will include ike/sip

            self.sipmsgs = list()





            #reg type
            self.regtype = 'udp'
            #seqdiag str
            self.diagstr = ""

            #record recompiled sip msg, which include more important msg
            self.diagsips = list()

            #record all entity UE or Network
            self.entities = list()

            #record all caller/calee using call-id to map
            #key is callid
            #NOTE: assume mo means left, mt means right...
            self.callidmapmomt = dict()

            #record each call-id's session flow: hold/resume/upgrade/downgrade... etc
            #key is callid
            self.callflow = dict()

            #record ue's num
            self.uenum = ''

            self.starttime = datetime.now()

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)


    def findmainlog(self, path):
        pass


    def getRegType(self, line):
        regpattern = re.compile(r'.*get register tpt type\<(.*)\>.*')
        match = regpattern.match(line)
        if not match:
            return
        regtype = int(match.group(1))
        if regtype == 0:
            self.regtype = 'udp'
        else:
            self.regtype = 'tcp'
        self.logger.logger.info('regtype is ' + self.regtype)


    def getSendSip(self,line,lineno):
        senddatalen =  self.getSendLen(line)
        if not senddatalen:
            self.logger.logger.error('no send data len in line ' + str(lineno))
            return

        #search backward
        found = 0
        searchstart = lineno - 1
        dataindex = lineno - 1
        #there may be race condition, receive two request at the same time
        #log may delay
        #NOTE: need to find pattern 'data length: 400' first
        datalenanchor = self.datalentags + str(senddatalen)

        while dataindex >= 0:
            if datalenanchor not in self.loglines[dataindex]:
                dataindex = dataindex - 1
            else:
                break
        self.logger.logger.debug('data anchor is ' + datalenanchor + ' , lineno is ' + str(dataindex))

        if dataindex < 0:
            self.logger.logger.error('no sip msg for line ' + line + ', lineno is '+ str(lineno))
            return

        while searchstart >= dataindex:
            if self.siptags in self.loglines[searchstart]:
                found +=1
                self.logger.logger.info('found send siptags in ' + str(searchstart) + ', found num is ' + str(found))
                if found == 1:
                    end =  searchstart
                    searchstart = searchstart - 1
                else:
                    start = searchstart
                    #record the timestamp
                    fields = self.loglines[searchstart].split(' ')
                    #04-17 23:21:24.420
                    timestamp = fields[0] + ' ' + fields[1]
                    break
            else:
                searchstart = searchstart - 1
        with open(self.lemonlog, 'a+') as llog:
            self.logger.logger.info('dump line from ' + str(start) + ' to ' + str(end))
            sendsip = dict()
            sendsip['send'] = True
            sendsip['lineno'] = lineno
            sendsip['timestamp'] = timestamp
            sendsip['msg'] = list()
            sendsip['issip'] = 1
            for pindex in range(start,end+1):
                sendsip['msg'].append(self.loglines[pindex])
                llog.write(self.loglines[pindex])
        self.logger.logger.error('current sipmsgs index is ' + str(len(self.sipmsgs)))
        self.sipmsgs.append(sendsip)


    def getRecvSip(self,line, lineno):
        recvdatalen = self.getRecvLen(line)
        if not recvdatalen:
            self.logger.logger.error('no recv data len in line ' + str(lineno))
            return
        #search forward
        #we have to search two siptags and write the lines between the two tags
        found = 0
        searchstart = lineno + 1
        dataindex = lineno + 1

        #there may be race condition, receive two request at the same time
        #log may delay
        #NOTE: need to find pattern 'data length: 400' first
        datalenanchor = self.datalentags + str(recvdatalen)
        self.logger.logger.error('data anchor is ' + datalenanchor)
        while dataindex >= 0 and dataindex < len(self.loglines):
            if datalenanchor not in self.loglines[dataindex]:
                dataindex = dataindex + 1
            else:
                break

        if dataindex == len(self.loglines):
            self.logger.logger.error("not sip msg for line " + line + ' , lineno  is '+ str(lineno))
            return;


        searchstart = dataindex
        while searchstart <=  len(self.loglines):
            if self.siptags in self.loglines[searchstart]:
                found += 1
                self.logger.logger.info('found recv siptags in ' + str(searchstart) + ', found num is ' + str(found))
                if found == 1:
                    start = searchstart
                    searchstart += 1
                else:
                    end = searchstart
                    #record the timestamp
                    fields = self.loglines[searchstart].split(' ')
                    #04-17 23:21:24.420
                    timestamp = fields[0] + ' ' + fields[1]
                    #if we found two siptags then break
                    break
            else:
                searchstart += 1

        with open(self.lemonlog, 'a+') as llog:
            self.logger.logger.info('dump line from ' + str(start) + ' to ' + str(end))
            recvsip = dict()
            recvsip['send'] = False
            recvsip['msg'] = list()
            recvsip['lineno'] = lineno
            recvsip['timestamp'] = timestamp
            recvsip['issip'] = 1
            #record req line and other fields here
            for pindex in range(start,end+1):
                recvsip['msg'].append(self.loglines[pindex])
                llog.write(self.loglines[pindex])
        self.sipmsgs.append(recvsip)

    def getikemsg(self, line, lineno):
        ikemsg = dict()
        ikemsg['issip'] = 0
        ikemsg['lineno'] = lineno
        fields = line.split(' ')
        #04-17 23:21:24.420
        timestamp = fields[0] + ' ' + fields[1]
        ikemsg['timestamp'] = timestamp

        ikemsg['msg'] = line
        ikemsg['verbosemsg'] = list()
        ikeparser = self.ikeParser
        msgheader = ikeparser.getIkeHeader(line)

        if msgheader:
           ikemsg['action'] = msgheader['action']
           ikemsg['content'] = msgheader['content']
           ikemsg['msgid'] = msgheader['msgid']
        else:
            self.logger.logger.error('not valid ike included in ' + line)


        #there is Encode/Decode end tag, copy start lineno to end tag lineno



        #the matching line
        endtag = ''
        if ikemsg['action'] == 'Decode':
            endtag = self.config['sprd']['ikedecodeendtags']
        else:
            endtag = self.config['sprd']['ikeencodeendtags']

        searchstart = lineno + 1
        endlineno = lineno + 1
        self.logger.logger.info('searchstart is ' + str(searchstart) + ', endtag is ' + endtag)
        while searchstart < len(self.loglines):
            #just search forward
            #self.logger.logger.error('searchstart is ' + str(searchstart))

            if endtag in self.loglines[searchstart]:
                endlineno = searchstart
                break
            else:
                searchstart += 1
        with open(self.lemonlog, 'a+') as llog:
            self.logger.logger.info('dump line from ' + str(lineno) + ' to ' + str(endlineno))

            for pindex in range(lineno-1,endlineno+1):
                ikemsg['verbosemsg'].append(self.loglines[pindex])
                llog.write(self.loglines[pindex])

        self.sipmsgs.append(ikemsg)

    #TODO: later may add event parser file?
    def searchEvent(self, line, lineno):
        for index, event in enumerate(EventArray):
            key = event['key']
            modulename = event['module']
            #later we may add pattern
            pattern = re.compile(key)
            match = pattern.search(line)
            if match:
                #now parse the line
                eventmsg = dict()
                fields = line.strip(' \t').split(' ')
                #04-17 23:21:24.420
                timestamp = fields[0] + ' ' + fields[1]
                eventmsg['timestamp'] = timestamp
                eventmsg['msg'] = line.strip(' \t')
                #event content is modulename + matchlog
                eventmsg['event'] = modulename + ' : ' + match.group(1)
                self.logger.logger.error('the target event is ' + eventmsg['event'])
                eventmsg['lineno'] = lineno
                eventmsg['issip'] = 0
                eventmsg['isevent'] = 1
                self.sipmsgs.append(eventmsg)
                break


    def getFlow(self):
        #first of all we get the whole important logs
        lpdaps = logParser(logname=self.log, filterlevel='low', outputdir=self.resultdir)
        self.keylogdaps= lpdaps.getflow(has_ps=False)


        # lpall = logParser(logname=self.log, filterlevel='high', outputdir=self.resultdir)
        #self.keylogall = lpall.getflow(has_ps=False)


        #rePattern = r'' + 'fsm(.*)' + ' | \[TIMER.*\]' + '|recv.*data' + '| process request' + '|process response'
        lemonpattern = self.utils.getPattern(self.lemontags)
        self.logger.logger.info('lemon pattern is ' + lemonpattern)
        if not lemonpattern:
            self.logger.logger.error('lemonpattern is none!')
            return

        sprdPattern = re.compile(lemonpattern)
        senderpattern = re.compile(r'' + self.sendertags)
        receiverpattern = re.compile(r'' +  self.receivertags)
        ikepattern = re.compile(r'' + self.iketags)


        self.logger.logger.info("all output will be redirected to " + self.lemonlog)
        with open(self.log, 'rb') as logfile:
            for lineno, line in enumerate(logfile):
                line = line.strip(' \t')
                self.getRegType(line)
                if sprdPattern.search(line):
                    with open(self.lemonlog, 'a+') as llog:
                        llog.write(line)

                #FIXME: there may be race condition
                #the data print can be different.
                #if it is receivertags, search forward
                if receiverpattern.search(line):
                    with open(self.lemonlog, 'a+') as llog:
                        llog.write(line)
                    self.getRecvSip(line, lineno)
                #if it is sendertags, search backward
                if senderpattern.search(line):
                    self.getSendSip(line, lineno)
                    with open(self.lemonlog, 'a+') as llog:
                        llog.write(line)

                if ikepattern.search(line):
                    self.getikemsg(line, lineno)

                #add function to detect event msg
                self.searchEvent(line, lineno)

        return len(self.sipmsgs)

    def drawDemoDiag(self):
        #http://blockdiag.com/en/seqdiag/examples.html
        diagram_definition = u"""
           seqdiag {
              browser  -> webserver [label = "GET /index.html"];
              browser <- webserver;
           }
        """
        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)
        draw = drawer.DiagramDraw('PNG', diagram, filename="diagram.png")
        draw.draw()
        draw.save()

    def getDataLen(self, pattern, line):
        lenpattern = re.compile(pattern)
        matchpattern = lenpattern.match(line)
        if not matchpattern:
            return None
        recvdatalen = int(matchpattern.group(1))
        return recvdatalen

    def getRecvLen(self, line):
        #first of all , check the recv data's length
        recvpattern = r'.*recv.*data\(len:(.*)\).*'
        recvdatalen = self.getDataLen(recvpattern, line)

        #FIXME: the 250 is some kind of exp value
        #IKE msg can be longer than 250
        if recvdatalen < 250:
            self.logger.logger.warn('receiving non-SIP msg, len is ' + str(recvdatalen))
            return None
        else:
            return recvdatalen


    def getSendLen(self, line):
        #get length
        sendpattern = r'.*send data\[(.*)\].*to.*'
        senddatalen = self.getDataLen(sendpattern, line)
        #FIXME: the 250 is some kind of exp value
        if senddatalen < 250:
            self.logger.logger.warn('send non-SIP msg , len is ' + str(senddatalen))
            return  None
        else:
            return senddatalen

    def getReqMethod(self, line):
        requestpattern = re.compile(".* process request \<(.*)\>.*")

        matchpattern = requestpattern.match(line)

        if not matchpattern:
            self.logger.logger.info("not match method line " + line + requestpattern)
            return None

        method = matchpattern.group(1)
        return method

    def getRspCode(self, line):
        rsppattern =  re.compile(".*process response \<(.*)\>.*")
        matchpattern = rsppattern.match(line)

        if not matchpattern:
            self.logger.logger.info("not match rsp pattern in  line " + line + rsppattern)
            return None

        rspmatch = matchpattern.group(1)
        rspcode = rspmatch.split(':')[1]
        rspstr =  rspmatch.split(':')[0]
        return str(rspcode) + ' for method ' + rspstr


    def searchRecv(self, lineno, file):
        #when "recv data", search forward
        #note: sip msg is usually larger than 250 bytes.
        #print line,
        line = self.lemonlines[lineno]
        recvdatalen = self.getRecvLen(line)

        if not recvdatalen:
            self.logger.logger.error('no recv data len in line' + str(lineno))
            return

        #start to search forward
        start = lineno+1
        requesttags = "process request"
        responsetags = "process response"

        while start <= len(self.lemonlines):
            waterline = self.lemonlines[start]
            if requesttags in waterline:
                #is request
                self.logger.logger.info(start,waterline, ' recv req')

                method = self.getReqMethod(waterline)
                if not method:
                    self.logger.logger.info('recv direction no request method in line ' + str(lineno))
                    return
                self.diagstr += "UE <- NETWORK [label = \"" + method + " No." + str(lineno)+"\"];\n"


                break;
            if responsetags in waterline:
                #is response
                self.logger.logger.info(start,waterline, ' recv rsp')

                rspstr = self.getRspCode(waterline)
                if not rspstr:
                    self.logger.logger.info('recv direction no rsp in line ' + str(lineno))
                    return

                self.diagstr += "UE <- NETWORK [label = \"" + rspstr + " No." + str(lineno)+"\"];\n"

                break;
            start += 1

    def searchSend(self, lineno, file):
        #when "UTPT.*send data", search backwards
        requesttags = "process request"
        responsetags = "process response"
        #non-invite ,invite udp timeout timer
        timeretags = "TIMER E"
        timeratags = "TIMER A"

        line = self.lemonlines[lineno]
        senddatalen = self.getSendLen(line)
        if not senddatalen:
            self.logger.logger.info('no send data len in line' + str(lineno))
            return
        #start to search backward
        start = lineno - 1
        while start >= 0:
            waterline = self.lemonlines[start]
            if timeretags in waterline:
                self.logger.logger.info(start, "retransmit previous non-invite request")
                self.diagstr += "UE -> NETWORK [label = \"retrans non-invite req" + " No." + str(lineno)+"\"];\n"
                break;
            if timeratags in waterline:
                self.logger.logger.info(start, "retransmit previous invite request")
                self.diagstr += "UE -> NETWORK [label = \"retrans invite req" + " No." + str(lineno)+"\"];\n"
                break;

            if requesttags in waterline:
                #is request
                self.logger.logger.info(start,waterline, ' send req')
                #get request method

                method = self.getReqMethod(waterline)
                if not method:
                    self.logger.logger.info('send direction no request method in line ' + str(lineno))
                    return
                self.diagstr += "UE -> NETWORK [label = \"" + method + " No." + str(lineno)+"\"];\n"
                break
            if responsetags in waterline:
                #is response
                self.logger.logger.info(start,waterline, ' send rsp')

                rspstr = self.getRspCode(waterline)
                if not rspstr:
                    self.logger.logger.info('send direction no rsp in line ' + str(lineno))
                    return

                self.diagstr += "UE -> NETWORK [label = \"" + rspstr + " No." + str(lineno)+"\"];\n"

                break;
            start = start - 1


    def parseFlowOld(self):
        '''
            obsoleted function, old function which will not be used any more
        :return:
        '''
        # NOTE:
        #     1. identify msg sender: UTPT.*send data/msg recviver: recv data
        #      Timer E's send data
        #      the magic is that:
        #             when "UTPT.*send data", search backwards; when "recv data", search forward
        #          for line in itertools.islice(text_file, start, end):

        senderpattern = re.compile(r'' + self.sendertags)
        receiverpattern = re.compile(r'' +  self.receivertags)

        #first we just cache all lines
        with open(self.lemonlog) as lemonlog:
            self.lemonlines = lemonlog.readlines()

        with open(self.lemonlog) as lemonlog:
            for lineno,line in enumerate(lemonlog):
                #big loop
                if receiverpattern.search(line):
                    self.searchRecv(lineno,  lemonlog)
                if senderpattern.search(line):
                    self.searchSend(lineno, lemonlog)


    def dumpDiagsip(self):
        '''
        use to dump all trimp sip with important info
        :return:
        '''
        for sipindex, sip in enumerate(self.diagsips):
            self.logger.logger.error('request index is ' + str(sipindex))
            for key,value in sip.iteritems():
                self.logger.logger.error(str(key) + ':' + str(value))

    def assembleDiagStrOld(self,diaginfo):
        #sample UE -> NETWORK [label = "200 OK", note = "Cseq 1 REGISTER\n lineno: 888"];
        if diaginfo['send']:
            direct = '->'
        else:
            direct = '<-'

        basedirect =  "UE " + direct + " NETWORK "
        label =  "[label = \"" + diaginfo['label'] + "\""

        timestamp = "\"time: " + diaginfo['timestamp'] + "\n"
        cseq = " CSeq: " + diaginfo['cseq'] + '\n'
        callid = " Call-ID: "+ diaginfo['callid'] + '\n'
        lineno = " lineno: " + str(diaginfo['lineno']) + "\""

        note = ", note = " + timestamp + cseq + callid+ lineno

        label = label + note + "];\n"
        #print label
        self.diagstr +=  basedirect + label

    def findUE(self):
        for sipindex, sip in enumerate(self.diagsips):
            if sip['issip']:
                if 'REGISTER' in sip['cseq']:
                    #add this special logic, there may be no 200 OK for Reg
                    cseqnum = sip['cseq'].split(' ')[0]
                    #self.logger.logger.error('cseqnum is ' + str(cseqnum) + ', fromnum is ' + str(sip['fromnum'])
                    if int(cseqnum) == 1:
                        self.uenum = sip['fromnum']


                    # use cseq:.*REGISTER to tell
                    #200 OK for REGISTER will include P-Associate-URI
                    if sip['pasonum']:
                        self.uenum = sip['pasonum']
                        break

                else:
                    #from the direction, can tell the ue's num
                    if sip['send']:
                        self.uenum = sip['fromnum']
                    else:
                        self.uenum = sip['tonum']
                    break

    def addElement(self, element):
        if element not in self.elements:
            self.elements.append(element)

    def assembleSipStr(self, sip, elements):
        callid = sip['callid']
        momt = ''

        momtlist = self.callidmapmomt[callid]
        if sip['b2bua']:
            momt = momtlist[1]
        else:
            momt = momtlist[0]


        if sip['send']:
            #NOTE: space is important
            direct = ' -> '
            #find left/right by callid

            leftnum = momt['mo']
            rightnum = momt['mt']
            left = elements[leftnum]
            right = elements[rightnum]
        else:
            #FIXME: if the msg has cause, only if the network send it to UE
            direct = ' <- '
            if sip['hascause']:
                left = elements[self.uenum]
                right = 'NETWORK'
            else:
                leftnum = momt['mo']
                rightnum = momt['mt']
                left = elements[leftnum]
                right = elements[rightnum]

        '''
        when we get new left, right, we check and added it in the self.elements
        '''
        self.addElement(left)
        self.addElement(right)

        #some color or string decoration
        # session modificaiton should be marked.
        #TODO: add seperator line for each call process: not needed here, call can be complex.
        sdpstring = ""
        action = ''
        mediadirection = ''
        labelcolor = ""
        notecolor =  ""

        basedirect =  left + direct + right
        label =  " [label = \"" + sip['label'] + "\""

        timestamp = "Time: " + sip['timestamp'] + "\n"
        if sip['issdp'] and sip['isinvite'] :
            action = "Action: " +  sip['action'] + '\n'

        #some critical msg should be marked as red
        if sip['b2bua'] or sip['hascause'] or sip['iserrorrsp']:
            labelcolor = ", color=red"

        sdpinfo = ''
        if sip['issdp']:
            sdpstring = " with sdp"
            self.logger.logger.error('error lineno is ' + str(sip['lineno']))
            if sip['isvideo'] and not sip['vdirect']:
                mediadirection += "video: " + sip['vdirect'] + ', port: '+ str(sip['vport']) +';'

            if sip['adirect']:
                mediadirection += 'audio: ' + sip['adirect'] + ', port: '+ str(sip['aport']) +'\n'

            if sip['codec']:
                for codec, codecvalue in sip['codec'].iteritems():
                    for sdpparam, value in codecvalue.iteritems():
                        sdpinfo += 'Codec ' + str(codec) + ': ' + sdpparam + ' ' + value  + '\n'



        elif sip['b2bua'] and sip['isinvite']:
            sdpstring = " without sdp"
            #B2BUA's request will be marked

        if sip['cause']:
            cause = ',' + str(sip['cause']['code']) + '/' + sip['cause']['isdn']
        else:
            cause = ''

        if sip['ua']:
            ua = " User-Agent: " + sip['ua'] + '\n'
        else:
            ua = ''

        if sip['retryafter']:
            retryafter = " Retry-After: " + sip['retryafter'] + '\n'
        else:
            retryafter = ''

        if sip['expires']:
            expires = " Expires: " + sip['expires'] + '\n'
        else:
            expires = ''

        if sip['pasouri']:
            pasouri = " P-Associate-Uri: " + sip['pasouri'] + '\n'
        else:
            pasouri = ''

        if sip['supported']:
            supported = " Supported: " + sip['supported'] + '\n'
        else:
            supported = ''


        if sip['require']:
            require = " Require: " + sip['require'] + '\n'
        else:
            require = ''


        if sip['paccess']:
            paccess = "P-Access-Network-Info: " + sip['paccess'] + '\n'
        else:
            paccess = ''


        note = " Note: " + sdpstring + cause + '\n'
        cseq = " CSeq: " + sip['cseq'] + '\n'
        #callid = " Call-ID: "+ sip['callid'] + '\n'
        fromtag = " From: " + sip['fromnum'] + '\n'
        totag = " To: " + sip['tonum'] + '\n'
        callid = " Call-ID: " + sip['callid'] + '\n'
        lineno = " log lineno: " + str(sip['lineno'])


        #sample
        #x_917011021641 -> NETWORK [label = "REGISTER", note = "Time: 06-23 13:21:13.922
        #CSeq: 1 REGISTER
        #Note:
        #From: 405872000010425
        #To: 405872000010425
        #Call-ID: Ic08Qn.CU6xke*qifx321ICCxI@[2405:204:3807:2ade::262e:28a0]
        #log lineno: 5249"];

        note = ", note = \"" + timestamp + cseq + action + note + mediadirection + sdpinfo + expires + pasouri + supported + require + ua + paccess + retryafter+ fromtag + totag + callid +lineno + "\""

        label = label + note + labelcolor + "];\n"
        #print label
        onestr =  basedirect + label
        return onestr

    def assembleIkeStr(self,ike, elements):

        if not self.uenum:
            left = 'UE'
        else:
            left = elements[self.uenum]
        right = elements['NETWORK']

        '''
        when we get new left, right, we check and added it in the self.elements
        '''
        self.addElement(left)
        self.addElement(right)

        if ike['send']:
            #CAUTION: the two spaces are important
            direct = ' -> '
        else:
            direct = ' <- '

        #simply parse spi/payload
        spi = ike['configpayload']['spi']
        payload = ike['configpayload']['config']

        basedirect =  left + direct + right
        label =  " [label = \"" + ike['content']  + "\""
        timestamp = "Time: " + ike['timestamp'] + "\n"
        msgid = "Message ID: " + ike['msgid'] + "\n"
        spii = "init spi: " + spi['spii'] + "\n"
        spir = "rsp spi: " + spi['spir'] + '\n'

        #add labelcolor
        labelcolor = ''
        if payload['isnotifyerror'] or payload['isdelete']:
            labelcolor = ", color=red"


        #add payload type
        payloadstr = ''
        if payload['payloadtype']:
            for index, payloadtype in enumerate(payload['payloadtype']):
                payloadstr += 'Type Payload: ' + payloadtype + '\n'
        #add notify msg which may contain error msg
        notifystr= ''
        if payload['notify']:
            for index, notifymsg in enumerate(payload['notify']):
                notifystr += "Notify Message Type: "+ notifymsg + '\n'

        lineno = " log lineno: " + str(ike['lineno'])

        if payload['ipv4']:
            ipv4 = "IPv4: " + payload['ipv4'] + "\n"
        else:
            ipv4 = ''

        if payload['ipv6']:
            ipv6 = "IPv6: " + payload['ipv6'] + "\n"
        else:
            ipv6 = ''

        if payload['dnsv4']:
            dnsv4 = "DNS v4: " + payload['dnsv4'] + "\n"
        else:
            dnsv4 = ''

        if payload['dnsv6']:
            dnsv6 = "DNS v6: " + payload['dnsv6'] + "\n"
        else:
            dnsv6 = ''

        if payload['pcscfipv4_1']:
            pcscfv4_1 = "PCSCF v4(1) : " + payload['pcscfipv4_1'] + '\n'
        else:
            pcscfv4_1 = ''

        if payload['pcscfipv4_2']:
            pcscfv4_2 = "PCSCF v4(2) : " + payload['pcscfipv4_2'] + '\n'
        else:
            pcscfv4_2 = ''

        if payload['pcscfipv6_1']:
            pcscfv6_1 = "PCSCF v6(1) : " + payload['pcscfipv6_1'] + '\n'
        else:
            pcscfv6_1 = ''

        if payload['pcscfipv6_2']:
            pcscfv6_2 = "PCSCF v6(2) : " + payload['pcscfipv6_2'] + '\n'
        else:
            pcscfv6_2 = ''

        configuration = ipv4 + ipv6 + \
               dnsv4 + dnsv6 + pcscfv4_1 + pcscfv4_2 + pcscfv6_1 + pcscfv6_2

        note = ", note = \"" + timestamp + msgid + spii + spir + payloadstr+ notifystr+ configuration + lineno + "\""

        label = label + note + labelcolor + "];\n"
        onestr = basedirect + label
        return onestr


    def assembleEventStr(self, event):
        #quite simple
        timestamp = event['timestamp']
        string = event['event']
        lineno = event['lineno']
        onestr = ' === ' + string + ', time: ' + str(timestamp) + ', lineno: '+ str(lineno)  + '=== \n'
        return onestr

    def assembleDiagStr(self):
        #first define all UE and network name
        elements = dict()
        #add stub for NETWORK
        elements['NETWORK'] = 'NETWORK'
        self.findUE()

        for index, entity in enumerate(self.entities):
            if entity == self.uenum:
                #seqdial's title do not support + char??!!
                elements[self.uenum] = entity.strip('+')
            else:
                elements[entity] = entity.strip('+')


        if self.uenum:
            self.logger.logger.info('ue name is '+ elements[self.uenum])


        #1. element order
        #2. get the UE's number
        #
        left = ''
        right = ''
        direct = ''


        #add one more loop to fix REGISTER req/rsp's mo and mt
        for sipindex, sip in enumerate(self.diagsips):
            if sip['issip']:
                callid = sip['callid']
                momtlist = self.callidmapmomt[callid]
                if 'REGISTER' in sip['cseq'] and sip['pasonum']:
                    self.logger.logger.info('use P-Associate-URI'+ str(sip['pasonum']) + ' for register ' + sip['fromnum'])
                    momtlist[0]['mo'] = sip['pasonum']

        splitnum = len(self.diagsips) / int(self.splitgate) + 1
        self.logger.logger.info('the diagsips will be divided into %d ' % splitnum)
        self.diagstrList = [''] * splitnum


        for sipindex, sip in enumerate(self.diagsips):

            sector = (sipindex + 1) / int(self.splitgate)
            if sip['issip']:
                self.logger.logger.info('index is '+str(sipindex)+ ', callid is ' + callid)
                onestr = self.assembleSipStr(sip, elements)
            else:
                if 'isevent' in sip:
                    onestr = self.assembleEventStr(sip)
                else:
                    #parse ike msg
                    onestr = self.assembleIkeStr(sip, elements)

            self.diagstr += onestr
            self.diagstrList[sector] += onestr

    def getRealNum(self,string):
        #FIXME: special handling for MESSAGE's deliver report
        # the num may be a address
        if self.sipparser.checkIp(string):
            return 'NETWORK'
        else:
             return string


    def dumpcallidmaping(self):
        for callid, momtlist in self.callidmapmomt.iteritems():
            self.logger.logger.error('callid is ' + str(callid))
            for i,val in enumerate(momtlist):
                self.logger.logger.error('index is '+ str(i))
                for  field, momtvalue in val.iteritems():
                   self.logger.logger.error('pair is ' + field + ':'+ momtvalue)


    def judgeSessionModify(self,sip):
        #for voice, next state can be upgrade video or hold/held(send/recv sendonly)
        #for video, next state can be downgrade voice or hold/held(send/recv sendonly)
        #for hold, can send 'sendrecv'(resume) or recv 'inactive'(held again...)
        '''
        LEMON sdp nego logic: seems magic
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        pstAsPu->ucNegoDir = EN_SDP_DIRECT_TYPE_NONE;
        if (pstAsPu->ucPeerDir & EN_SDP_DIRECT_TYPE_RECV)
            pstAsPu->ucNegoDir |= EN_SDP_DIRECT_TYPE_SEND;
        if (pstAsPu->ucPeerDir & EN_SDP_DIRECT_TYPE_SEND)
            pstAsPu->ucNegoDir |= EN_SDP_DIRECT_TYPE_RECV;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        callid = sip['callid']
        flowdata = self.callflow[callid]

        lastcnt = 0
        lastaction = ''
        #last action
        if int(flowdata['cnt']) > 0:
            lastcnt = int(flowdata['cnt']) - 1
            lastaction = flowdata['flow'][lastcnt]
            self.logger.logger.error('last action is ' + lastaction)


        if sip['isvideo'] and sip['vport'] != str(0):
         # if video
            if not lastaction:
                sip['action'] = 'Video Call'
                return

            if sip['vdirect'] == 'sendonly':
                sip['action'] = 'Hold'
            elif sip['vdirect'] == 'inactive':
                #already held, but to hold remote
                sip['action'] = 'Hold'
            elif sip['vdirect'] == 'recvonly':
                sip['action'] = 'Resume'
            elif sip['vdirect'] == 'sendrecv' and lastaction == 'Hold':
                sip['action'] = 'Resume'
            else:
                sip['action'] = 'Video Call'

        else:
         # if voice
            if not lastaction:
                sip['action'] = 'Voice Call'
                return

            if sip['adirect'] == 'sendonly':
                sip['action'] = 'Hold'
            elif sip['adirect'] == 'inactive':
                #already held, but to hold r
                sip['action'] == 'Hold'
            elif sip['adirect'] == 'recvonly':
                sip['action'] = 'Resume'
            elif sip['adirect'] == 'sendrecv' and lastaction == 'Hold':
                sip['action'] = 'Resume'
            else:
                sip['action'] = 'Voice Call'


    def analyzeSdp(self, sip, index):

        callid = sip['callid']
        #init the callflow
        if callid not in self.callflow:

            self.callflow[callid] = dict()
            #session modificatin count
            self.callflow[callid]['cnt'] = 0
            #record last sip to avoid retransmit
            self.callflow[callid]['lastinvite'] = dict()
            #list with each session modification
            self.callflow[callid]['flow'] = list()

        lastinvite = self.callflow[callid]['lastinvite']
        #       1. only should scan invite
        #       2. record the same callerid's action flow.
        if sip['sdp'] :
            sip['isvideo'] = False
            sip['adirect'] = 'sendrecv'
            sip['vdirect'] = ''
            sipparser = self.sipparser
            for index, sdpline in enumerate(sip['sdp']):
                #1. check media:          m=audio 37042 RTP/AVP 104 0 8 116 103 9 101
                #2. check media redirect: a=sendrecv
                #3. add rtpmap, fmtp

                mediadict = sipparser.getmedia(sdpline)
                direct = sipparser.getsdpDirect(sdpline)
                rtpmap = sipparser.getrtpmap(sdpline)
                fmtp = sipparser.getfmtp(sdpline)

                if mediadict:
                    if mediadict['mtype'] == 'video':
                        self.logger.logger.debug('found video')
                        sip['isvideo'] = True
                        sip['vport'] = mediadict['mport']
                    else:
                        sip['isvideo'] = False
                        sip['aport'] = mediadict['mport']
                elif direct:
                    #assume that the voice attribute comes first and video later
                    if sip['isvideo'] :
                        self.logger.logger.debug('video direct is ' + direct)
                        sip['vdirect'] = direct
                    else:
                        sip['adirect'] = direct
                        self.logger.logger.debug('audio direct is ' + direct)
                elif rtpmap:
                    payload = rtpmap['payload']
                    value = rtpmap['rtpmap']
                    if payload not in sip['codec']:
                        sip['codec'][payload] = dict()

                    sip['codec'][payload]['rtpmap'] = value
                elif fmtp:
                    payload = fmtp['payload']
                    value = fmtp['fmtp']
                    if payload not in sip['codec']:
                        sip['codec'][payload] = dict()
                    sip['codec'][payload]['fmtp'] = value

         #now get the conclusion: voice/video/hold/resume


            if sip['isinvite']:
                self.logger.logger.info('start to judge session modification for index ' + str(index))
                self.judgeSessionModify(sip)
                #increase the count
                self.callflow[callid]['cnt'] += 1
                self.callflow[callid]['lastinvite'] = sip
                self.callflow[callid]['flow'].append(sip['action'])



    def analyzeSip(self):
        #get all UE's phone number,
        #check if reinivte does not have sdp

        #rules are listed below:
        # 1. only invite has 'fromnum', 'tonum'
        # 2. use call-id to identify the caller/callee
        # 3. TODO: MESSAGE should be parsed
        # 4: SUBSCRIBE/NOTIFY
        # 5: REGISTER
        # 6: sdp should be parsed
        # 7: tell B2BUA

        #NOTE: add logic to check B2BUA's msg
        # 1. once found b2bua, record/update Cseq and callid
        # 2. compare following signaling
        b2buarecord = dict()
        b2buarecord['cseq'] = ''
        b2buarecord['callid'] = ''

        for sipindex, sip in enumerate(self.diagsips):

            #add logic to identify msg not related to sip
            if not sip['issip']:
                continue




            fromnum = sip['fromnum']
            tonum = sip['tonum']
            callid = sip['callid']

            #f:<sip:10.56.4.9>;tag=6cV1ACafY7ic..fA
            #from can be ip
            if self.sipparser.checkIp(fromnum) == False:
                if fromnum not in self.entities:
                    self.entities.append(fromnum)
            if self.sipparser.checkIp(tonum) == False:
                if tonum not in self.entities:
                    self.entities.append(tonum)
            momt = dict()
            #store list of two
            momtlist = [dict()] * 2

            #IMPORTANT: record ]caller and callee via call-id

            #we will do the merge in momtlist
            if callid in self.callidmapmomt:
                momtlist = self.callidmapmomt[callid]


            #all 100 Trying/200OK/ACK about B2BUA, change its b2bua flag
            if callid == b2buarecord['callid']:
                if sip['cseq'] == b2buarecord['cseq']:
                    sip['b2bua'] = True
                else:

                    #FIXME: this logic is not correct here, there can be later ACK which is not about b2bua
                    '''
                    #NOTE: sometimes B2BUA's ACK not including "P-Com.Nokia.B2BUA-Involved"
                    cseqnum = b2buarecord['cseq'].split(' ')[0]
                    cseqack = cseqnum + ' ACK'


                    if sip['cseq'] == cseqack:
                        self.logger.logger.error('weird B2BUA\'s ACK not including P-Com.Nokia.B2BUA-Involved')
                        sip['b2bua'] = True
                    '''

            #FIXME: add logic to fix following b2buarecord
            if callid not in self.callidmapmomt or sip['b2bua']:
                #NOTE: here IMPU is set as mo
                if sip['isregister']:
                    momt['mo'] =  self.getRealNum(fromnum)
                    momt['mt'] = 'NETWORK'

                elif sip['issubs']:
                    #NOTIFY, SUBSCRIBE
                    momt['mo'] = self.getRealNum(fromnum)
                    momt['mt'] = 'NETWORK'
                #NOTE: B2BUA's callid is the same
                elif sip['b2bua']:
                    b2buarecord['callid'] = sip['callid']
                    b2buarecord['cseq'] = sip['cseq']
                    #mo always means left side, mt always means right side
                    momt['mo'] = self.getRealNum(tonum)
                    momt['mt'] = 'NETWORK'

                elif callid == b2buarecord['callid'] and sip['cseq'] == b2buarecord['cseq']:
                    if sip['send']:
                        momt['mo'] = self.getRealNum(fromnum)
                        momt['mt'] = 'NETWORK'
                    else:
                        momt['mo'] = self.getRealNum(tonum)
                        momt['mt'] = 'NETWORK'

                else:

                    #there is one bug in main log,
                    #UTPT.*send data may be missing, and mo, mt can be confused.
                    #because current rule assumes that the first occurence of the call-id's from to
                    #see logic in analyzeSip
                    #to work around this, add logci to check if this request is the first request of the call-id
                    # if not , missing log happens!!!
                    cseq = sip['cseq']
                    method = cseq.split(' ')[1]
                    logmissing = False
                    if method != sip['label']:
                        #check if it is the first request
                        self.logger.logger.error('there is log missing for callid ' + str(callid))
                        logmissing = True

                    if sip['send']:
                        if logmissing:
                            momt['mo'] = self.getRealNum(tonum)
                            momt['mt'] = self.getRealNum(fromnum)
                        else:
                            momt['mo'] = self.getRealNum(fromnum)
                            momt['mt'] = self.getRealNum(tonum)

                    else:
                        if logmissing:
                            momt['mo'] = self.getRealNum(fromnum)
                            momt['mt'] = self.getRealNum(tonum)
                        else:
                            momt['mo'] = self.getRealNum(tonum)
                            momt['mt'] = self.getRealNum(fromnum)

                if sip['b2bua']:
                    momtlist[1] = momt
                else:
                    momtlist[0] = momt

                #add dump here
                for i,val in enumerate(momtlist):
                    self.logger.logger.error('index is ' + str(sipindex) +' callid is '+ str(callid))
                    for  field, momtvalue in val.iteritems():
                        self.logger.logger.error('pair is ' + field + ':'+ momtvalue)

                self.callidmapmomt[callid] = momtlist
            #add logic to parser sdp
            self.analyzeSdp(sip, sipindex)


        #print 'entities num is ' + str(len(self.entities))
        #print 'callid num is ' + str(len(self.callids))
        #dump all the entities
        for index, entity in enumerate(self.entities):
            self.logger.logger.debug('participant_' + str(index) + ' is ' + entity)

        self.dumpcallidmaping()


    def diagSip(self, sipobj,index):
        sipparser = self.sipparser
        lineno = sipobj['lineno']
        timestamp = sipobj['timestamp']
        #1. get direction
        if sipobj['send'] == True:
            direct = '->'
        else:
            direct = '<-'
        #2. parse the sip, it is also a list
        sip = sipobj['msg']
        diaginfo = dict()
        diaginfo['isinvite'] = False
        diaginfo['isregister'] = False
        diaginfo['issdp'] = False
        diaginfo['issubs'] = False
        diaginfo['issdp'] = False
        diaginfo['pasonum'] = ''
        diaginfo['b2bua'] = False
        diaginfo['send'] = sipobj['send']
        diaginfo['sdp'] = list()
        diaginfo['issip'] = 1

        #add codec info
        diaginfo['codec'] = dict()

        #add flag if is error rsp
        diaginfo['iserrorrsp'] = False
        #add ua
        diaginfo['ua'] = ''
        #add retry-after
        diaginfo['retryafter'] = ''

        #add expires, supported, require, p-access-network-info, P-Associated-URI
        diaginfo['expires'] = None
        diaginfo['supported'] = None
        diaginfo['require'] = None
        diaginfo['paccess'] = None
        diaginfo['pasouri'] = None #is different from pasonum

        diaginfo['hascause'] = False
        diaginfo['cause'] = dict()

        #sdp record
        sdpstartindex = 0

        for msgindex,header in enumerate(sip):
            #get reqeust line/status line, other header

            method = sipparser.getMethod(header)
            if method:
                self.logger.logger.debug('found method ' + method  + ' in ' + str(index) + ' sip msg')
                diaginfo['lineno'] = lineno
                diaginfo['label'] =  method
                diaginfo['timestamp'] = timestamp
                #if method is INVITE, check Call-ID and From, to
                #OPTIONS/UPDATE/INFO/REFER/MESSAGE behaviour follow Invite's From/To
                if method == 'INVITE':
                    diaginfo['isinvite'] = True
                    continue

                if method == 'REGISTER' :
                    diaginfo['isregister'] = True
                    continue

                if method == 'SUBSCRIBE' or method == 'NOTIFY' or method == 'PUBLISH':
                    diaginfo['issubs'] = True
                    continue

            status = sipparser.getStatusLine(header)

            if status:
                diaginfo['lineno'] = lineno
                diaginfo['label'] = status['code'] + ' ' + status['phrase']
                self.logger.logger.debug('found status ' + diaginfo['label'] + ' in ' +  str(index) + ' sip msg')
                diaginfo['timestamp'] = timestamp
                #check if bad request
                if int(status['code']) >= 400:
                    diaginfo['iserrorrsp'] = True
                continue

            if 'callid' not in diaginfo:
                callid = sipparser.getHeaderContent(header, 'Call-ID')
                if callid:
                    diaginfo['callid'] = callid
                    continue

            if 'from' not in diaginfo:
                fromtag = sipparser.getHeaderContent(header, 'From')
                if fromtag:
                    diaginfo['from'] = fromtag
                    num = sipparser.getNumber(fromtag)
                    diaginfo['fromnum'] = num
                    continue

            if 'to' not in diaginfo:
                totag = sipparser.getHeaderContent(header, 'To')
                if totag:
                    diaginfo['to'] = totag
                    num = sipparser.getNumber(totag)
                    diaginfo['tonum'] = num
                    continue


            #some kind of hack code here, pasonum and pasouri come into the same loop.
            pasouri = sipparser.getHeaderContent(header, "P-Associated-URI")
            if pasouri:
                if not diaginfo['pasouri']:
                    diaginfo['pasouri'] = pasouri
                    #only get the first one split by comma
                    firstone = pasouri.split(',')[0]
                    diaginfo['pasonum'] = sipparser.getNumber(firstone)
                else:
                    diaginfo['pasouri'] += ',' + pasouri
                continue


            cseq = sipparser.getCSeq(header)
            if cseq:
                self.logger.logger.debug('found cseq ' + cseq  + ' in ' + str(index) + ' sip msg')
                diaginfo['cseq'] = cseq
                continue

            contenttype = sipparser.getHeaderContent(header, 'Content-Type')
            if contenttype:
                #sdp's Content-Type is application/sdp
                if 'application/sdp' in header:
                    diaginfo['issdp'] = True
                    self.logger.logger.debug('found sdp ' + ' in ' + str(index) +  ' sip msg')

            #check if is B2BUA
            b2buaflag = sipparser.checkB2BUA(header)
            if b2buaflag:
                diaginfo['b2bua'] = True

            cause = sipparser.getCause(header)
            if cause:
                diaginfo['hascause'] = True
                diaginfo['cause'] = cause #Two member: code ,isdn
                self.logger.logger.error('cause code is ' + str(cause['code']) + ', string is ' + cause['isdn'] )
                continue

            #add logic to record User-Agent
            ua = sipparser.getHeaderContent(header, 'User-Agent')
            if ua:
                diaginfo['ua'] = ua
            #add logci to record Retry-After
            retryafter = sipparser.getHeaderContent(header, 'Retry-After')
            if retryafter:
                diaginfo['retryafter'] = retryafter
                continue

            expires =  sipparser.getExpires(header)
            if expires:
                diaginfo['expires'] = expires
                continue

            #Supported/Require can be one line or multiple line...
            supported = sipparser.getHeaderContent(header, "Supported")
            if supported:
                if not diaginfo['supported']:
                    diaginfo['supported'] = supported
                else:
                    diaginfo['supported'] += ',' + supported
                continue

            require = sipparser.getHeaderContent(header, "Require")
            if require:
                if not diaginfo['require']:
                    diaginfo['require'] = require
                else:
                    diaginfo['require'] += ',' + require
                continue

            paccess = sipparser.getHeaderContent(header, "P-Access-Network-Info")
            if paccess:
                diaginfo['paccess'] = paccess
                continue


            #add logic to record sdp body
            sdppair = sipparser.sdpParser(header)
            if sdppair:
                if sdppair['type'] == 'v':
                    #record start line
                    sdpstartindex = msgindex

        if diaginfo['issdp']:
            diaginfo['sdp'] = sip[sdpstartindex:]
            #self.logger.logger.debug(diaginfo['sdp']);

        #add function to construct the diagram string
        self.diagsips.append(diaginfo)
        #oboselete logic
        #if diaginfo:
            #self.assembleDiagStrOld(diaginfo)

    def diagIke(self,ikeobj, index):
        #FIXME: IKE msg may still change
        ikeparser = self.ikeParser
        lineno = ikeobj['lineno']
        timestamp = ikeobj['timestamp']

        msg = ikeobj['msg']
        #detailed msg of ike
        vmsg = ikeobj['verbosemsg']

        #ike log is not well organized, just parse the final payload config.

        diaginfo = dict()
        diaginfo['issip'] = 0
        diaginfo['timestamp'] = ikeobj['timestamp']
        diaginfo['lineno'] = ikeobj['lineno']
        diaginfo['action'] = ikeobj['action']
        diaginfo['content'] = ikeobj['content']
        diaginfo['msgid'] = ikeobj['msgid']

        diaginfo['configpayload'] = dict()

        diaginfo['configpayload'] = ikeparser.getikepayload(vmsg)

        if diaginfo['action'] == 'Decode':
            diaginfo['send'] = False
        else:
            diaginfo['send'] = True

        self.diagsips.append(diaginfo)

    def diagEvent(self, eventobj, index):
        line = eventobj['msg']
        diaginfo = dict()
        diaginfo['issip'] = 0
        diaginfo['isevent'] = 1
        diaginfo['timestamp'] = eventobj['timestamp']
        diaginfo['lineno'] = eventobj['lineno']
        #TODO: may add more parsing logic here
        diaginfo['event'] = eventobj['event']

        self.diagsips.append(diaginfo)

    def parseFlow(self):
        '''
            generate the diag from self.sipmsgs
        :return:
        '''

        for index, sipobj in enumerate(self.sipmsgs):
            if sipobj['issip']:
                self.diagSip(sipobj, index)
            else:
                if 'isevent' in sipobj:
                    self.diagEvent(sipobj,index)
                else:
                    self.diagIke(sipobj, index)



        #analyze the trim sip
        self.analyzeSip()
        #dump the trim sip
        self.dumpDiagsip()
        if self.diagsips:
            self.assembleDiagStr()

    def drawAllDiag(self):
        estimatetime = 0.2 * int(len(self.sipmsgs))
        self.logger.logger.info('length of all msgs is ' + str(len(self.sipmsgs)) + ' may take ' + str(estimatetime) + ' seconds')

        for index, diagstr in enumerate(self.diagstrList):
            self.drawOneDiag(diagstr, index)

        #do the merge.
        merger = PdfFileMerger()
        for filename in self.pdfList:
            merger.append(PdfFileReader(file(filename, 'rb')))

        basename = os.path.basename(self.log)
        finalpdfname = self.diagdir + basename.split('.')[0] + '.pdf'
        merger.write(finalpdfname)
        self.endtime = datetime.now()
        self.duration = self.endtime - self.starttime
        self.logger.logger.info('length of all msgs is ' + str(len(self.sipmsgs)) + '  takes ' + str(self.duration) + ' seconds')
        #now need to do this
        #self.drawOneDiag(self.diagstr,'whole')

    def drawOneDiag(self, diagstr, postfix):
        '''
        used to draw only one piece of pdf
        :param diagstr:
        :return:
        '''
        diagram_definition = u"""seqdiag {\n"""
        #Set fontsize.
        #http://blockdiag.com/en/blockdiag/attributes/diagram.attributes.html
        diagram_definition += " default_fontsize = 16;\n"
        diagram_definition += " node_width = 155;\n"
        diagram_definition += " edge_length = 300;\n"
        #Do not show activity line
        diagram_definition += " activation = none;\n"
        #Numbering edges automaticaly
        diagram_definition += " autonumber = True;\n"


        #add elements
        # UE; NETWORK; UE1;
        for index, element in enumerate(self.elements):
            diagram_definition += element + ';'

        diagram_definition += '\n'

        diagram_definition += diagstr
        diagram_definition += u""" }\n"""
        # generate the diag string and draw it
        #self.logger.logger.info('seqdiag is ' + diagram_definition)
        #write the diagram string to file
        basename = os.path.basename(self.log)
        #print self.diagdirdiag + '\n'
        diagname = self.diagdirdiag + basename.split('.')[0] + '_' + str(postfix) + '.diag'
        #print diagname + '\n'
        pdfname = self.diagdirpdf + basename.split('.')[0] + '_' + str(postfix) + '.pdf'

        self.pdfList.append(pdfname)

        with open(diagname, 'w') as diagfile:
            diagfile.write(diagram_definition)
        #
        #self.utils.setup_imagedraw()
        #self.utils.setup_plugins()
        self.utils.setup_imagedraw()
        self.utils.setup_noderenderers()
        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)

        estimatetime = 0.2 * int(self.splitgate)
        self.logger.logger.info('generation sector '+ str(postfix) + ', may take ' + str(estimatetime) + ' s')
        #set the font info
        options = dict()
        options['fontmap'] = ''
        options['font'] = list()
        options['font'].append(path + '/font/DejaVuSerif.ttf:1')
        options = utils.dotdict(options)
        fm = create_fontmap(options)
        pdfdraw = drawer.DiagramDraw('PDF', diagram, filename=pdfname, debug=True, fontmap=fm)
        pdfdraw.draw()
        pdfdraw.save()

        #mv the png to right dir
        #os.rename(pngname, self.diagdir)



    ##FIXME: actually we use drawOneDiag now..., we do not use it now
    def drawLemonDiag(self):
        diagram_definition = u"""seqdiag {\n"""
        #Set fontsize.
        #http://blockdiag.com/en/blockdiag/attributes/diagram.attributes.html
        diagram_definition += " default_fontsize = 16;\n"
        diagram_definition += " node_width = 155;\n"
        diagram_definition += " edge_length = 300;\n"
        #Do not show activity line
        diagram_definition += " activation = none;\n"
        #Numbering edges automaticaly
        diagram_definition += " autonumber = True;\n"


        #add elements
        # UE; NETWORK; UE1;
        elementstr = ''
        for index, element in enumerate(self.elements):
            elementstr += element + ';'

        if not elementstr:
            elementstr = "UE; NETWORK;"
        diagram_definition +=elementstr + '\n'



        diagram_definition += self.diagstr
        diagram_definition += u""" }\n"""
        # generate the diag string and draw it
        self.logger.logger.info('seqdiag is ' + diagram_definition)
        #write the diagram string to file
        basename = os.path.basename(self.log)
        pngname = basename.split('.')[0] + '.png'
        diagname = basename.split('.')[0] + '.diag'
        pngname = self.diagdir + pngname
        pdfname = self.diagdir+ basename.split('.')[0] + '.pdf'
        diagname = self.diagdir + diagname
        with open(diagname, 'w') as diagfile:
            diagfile.write(diagram_definition)

        '''
        FIXME: can not workaround this bug
        https://groups.google.com/forum/embed/#!topic/blockdiag-discuss/9rUQwZXay0k
        pkg_resources is not supported in pyinstaller.

        #generate the diagram using exe/binary
        plat = platform.system()
        self.logger.logger.info('os type is ' + plat)
        if plat == 'Windows':
            subprocess.call(['./seqdiag.exe', '--debug',diagname])
        elif plat == 'Linux':
            subprocess.call(['./seqdiag', '--debug', diagname])
        else:
            self.logger.logger.error('do not support ' + plat)
        '''
        #
        #self.utils.setup_imagedraw()
        #self.utils.setup_plugins()
        self.utils.setup_imagedraw()
        self.utils.setup_noderenderers()


        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)

        self.logger.logger.info('diagram file is ' + pngname)
        estimatetime = 0.4 * len(self.sipmsgs)
        self.logger.logger.info('length of all msgs is ' + str(len(self.sipmsgs)) + ', may take ' + str(estimatetime) + ' s')
        #set the font info
        options = dict()
        options['fontmap'] = ''
        options['font'] = list()
        options['font'].append(path + '/font/DejaVuSerif.ttf:1')
        options = utils.dotdict(options)
        fm = create_fontmap(options)

        '''
        png takes much memory ,disable now.
        draw = drawer.DiagramDraw('PNG', diagram, filename=pngname, debug=True)
        draw.draw()
        draw.save()
        '''
        '''
        do not use svg
        svgdraw = drawer.DiagramDraw('SVG', diagram, filename=svgname, debug=True, fontmap=fm)
        svgdraw.draw()
        svgdraw.save()
        '''

        pdfdraw = drawer.DiagramDraw('PDF', diagram, filename=pdfname, debug=True, fontmap=fm)
        pdfdraw.draw()
        pdfdraw.save()

        #mv the png to right dir
        #os.rename(pngname, self.diagdir)
        self.endtime = datetime.now()
        self.duration = self.endtime - self.starttime
        self.logger.logger.info('length of all msgs is ' + str(len(self.sipmsgs)) + '  takes ' + str(self.duration) + ' seconds')

if __name__ == '__main__':
    fp = flowParser(logname='./0-main-06-07-12-09-45.log')
    fp.getFlow()
    fp.parseFlow()
    #later will use other drawDiag
    fp.drawLemonDiag()

    #fp.drawDemoDiag()
    #fp.parseFlowOld()
    #print len(fp.sipmsgs)
