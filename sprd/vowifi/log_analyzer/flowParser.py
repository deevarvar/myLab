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
1. seqdiag
2. dig into sip message
3. add record of previous send msg
4. mkdir for each log



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



class flowParser():
    def __init__(self):
        try:
            configfile = 'config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.lemontags = config['sprd']['lemontags']
            self.servicetags = config['sprd']['servicetags']
            self.adaptertags = config['sprd']['adaptertags']
            self.sendertags = config['sprd']['sendertags']
            self.receivertags =  config['sprd']['receivertags']

            self.files = dict()
            self.files['log'] = config['files']['log']
            print self.files['log']
            logList = glob.glob(self.files['log'])
            if not logList:
                print 'no log file found.'
                return
            self.log = logList[0]
            self.lemonlog = 'lemon_' +  self.log
            with open(self.lemonlog, 'w') as tlog:
                tlog.truncate()

            #reg type
            self.regtype = 'udp'
            #seqdiag str
            self.diagstr = ""
        except (ConfigObjError, IOError) as e:
             print('Could not read "%s": %s' % (configfile, e))

    def getPattern(self, taglist):
        if taglist :
            pattern = r''
            tagtype = type(taglist)
            if tagtype is list:
                for i,tag in enumerate(taglist):
                    pattern += str(tag) + '|'
                pattern = pattern[:len(pattern)-1]
            else:
                pattern += taglist
            return pattern
        else:
            print 'tags is empty'
            return None

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
        print 'regtype is ' + self.regtype

    def getFlow(self):
        #rePattern = r'' + 'fsm(.*)' + ' | \[TIMER.*\]' + '|recv.*data' + '| process request' + '|process response'
        lemonpattern = self.getPattern(self.lemontags)
        print 'lemon pattern is ' + lemonpattern
        if not lemonpattern:
            print 'lemonpattern is none!'
            return
        sprdPattern = re.compile(lemonpattern)
        print "all output will be redirected to " + self.lemonlog
        with open(self.log) as logfile:
            for lineno, line in enumerate(logfile):
                self.getRegType(line)
                if sprdPattern.search(line):
                    with open(self.lemonlog, 'a+') as llog:
                        llog.write(str(lineno) + " " + line)
                    #TODO: add logic to add sip msg


    def drawDemoDiag(self):
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

    def getReqMethod(self, line):
        requestpattern = re.compile(".* process request \<(.*)\>.*")

        matchpattern = requestpattern.match(line)

        if not matchpattern:
            print "not match method line", line, requestpattern
            return None

        method = matchpattern.group(1)
        return method

    def getRspCode(self, line):
        rsppattern =  re.compile(".*process response \<(.*)\>.*")
        matchpattern = rsppattern.match(line)

        if not matchpattern:
            print "not match rsp pattern in  line", line, rsppattern
            return None

        rspmatch = matchpattern.group(1)
        rspcode = rspmatch.split(':')[1]
        rspstr =  rspmatch.split(':')[0]
        return str(rspcode) + ' for method ' + rspstr


    def searchRecv(self, lineno, file):
        #when "recv data", search forward
        #note: sip msg is usually larger than 250 bytes.
        #print line,
        #first of all , check the recv data's length
        line = self.filelines[lineno]
        print lineno,line,

        recvpattern = r'.*recv.*data\(len:(.*)\).*'
        recvdatalen = self.getDataLen(recvpattern, line)

        if not recvdatalen:
            print 'no recv data len in line' + str(lineno)
            return
        #FIXME: the 250 is some kind of exp value
        if recvdatalen < 250:
            print 'receiving non-SIP msg, len is ' + str(recvdatalen) + ', in line ' + str(lineno)
            return
        #start to search forward
        start = lineno+1
        requesttags = "process request"
        responsetags = "process response"

        while start <= len(self.filelines):
            waterline = self.filelines[start]
            if requesttags in waterline:
                #is request
                print start,waterline, ' recv req'

                method = self.getReqMethod(waterline)
                if not method:
                    print 'recv direction no request method in line ' + str(lineno)
                    return
                self.diagstr += "UE <- NETWORK [label = \"" + method + " No." + str(lineno)+"\"];\n"


                break;
            if responsetags in waterline:
                #is response
                print start,waterline, ' recv rsp'

                rspstr = self.getRspCode(waterline)
                if not rspstr:
                    print 'recv direction no rsp in line ' + str(lineno)
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

        line = self.filelines[lineno]
        #get length
        sendpattern = r'.*send data\[(.*)\].*to.*'
        senddatalen = self.getDataLen(sendpattern, line)
        if not senddatalen:
            print 'no send data len in line' + str(lineno)
            return

        #FIXME: the 250 is some kind of exp value
        if senddatalen < 250:
            print 'send non-SIP msg , len is ' + str(senddatalen) + ', in line ' + str(lineno)
            return
        #start to search backward
        print lineno,line,
        start = lineno - 1
        while start >= 0:
            waterline = self.filelines[start]
            if timeretags in waterline:
                print start, "retransmit previous non-invite request"
                self.diagstr += "UE -> NETWORK [label = \"retrans non-invite req" + " No." + str(lineno)+"\"];\n"
                break;
            if timeratags in waterline:
                print start, "retransmit previous invite request"
                self.diagstr += "UE -> NETWORK [label = \"retrans invite req" + " No." + str(lineno)+"\"];\n"
                break;

            if requesttags in waterline:
                #is request
                print start,waterline, ' send req'
                #get request method

                method = self.getReqMethod(waterline)
                if not method:
                    print 'send direction no request method in line ' + str(lineno)
                    return
                self.diagstr += "UE -> NETWORK [label = \"" + method + " No." + str(lineno)+"\"];\n"
                break
            if responsetags in waterline:
                #is response
                print start,waterline, ' send rsp'

                rspstr = self.getRspCode(waterline)
                if not rspstr:
                    print 'send direction no rsp in line ' + str(lineno)
                    return

                self.diagstr += "UE -> NETWORK [label = \"" + rspstr + " No." + str(lineno)+"\"];\n"

                break;
            start = start - 1

    def parseFlow(self):
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
            self.filelines = lemonlog.readlines()
        with open(self.lemonlog) as lemonlog:
            for lineno,line in enumerate(lemonlog):
                #big loop
                if receiverpattern.search(line):
                    self.searchRecv(lineno,  lemonlog)
                if senderpattern.search(line):
                    self.searchSend(lineno, lemonlog)

                pass

    def drawLemonDiag(self):
        diagram_definition = u"""seqdiag {"""

        diagram_definition += self.diagstr
        diagram_definition += u""" }"""
        # generate the diag string and draw it
        print diagram_definition
        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)
        draw = drawer.DiagramDraw('PNG', diagram, filename="diagram.png")
        draw.draw()
        draw.save()
        pass

if __name__ == '__main__':
    fp = flowParser()
    fp.getFlow()
    #fp.drawDemoDiag()
    fp.parseFlow()
    fp.drawLemonDiag()
