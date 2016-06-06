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


#3. add a basic ui
#4. add a html page file


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
from time import gmtime, strftime
import logging

#add user defined lib
sys.path.append('./lib')
from SipParser import SipParser
from logConf import logConf
path = os.path.dirname(os.path.realpath(__file__))



class flowParser():
    def __init__(self):

        try:
            self.timestamp = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
            self.logpath = './' + str(self.timestamp) + '.log'
            configfile = path + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.lemontags = config['sprd']['lemontags']
            self.servicetags = config['sprd']['servicetags']
            self.adaptertags = config['sprd']['adaptertags']
            self.sendertags = config['sprd']['sendertags']
            self.receivertags =  config['sprd']['receivertags']
            self.siptags = config['sprd']['siptags']
            self.datalentags = config['sprd']['datalentags']
            self.loglevel =  config['logging']['loglevel']

            #have to set loglevel to interger...
            self.logger = logConf(logpath=self.logpath, debuglevel=logging.getLevelName(self.loglevel))
            self.sipparser = SipParser(configpath='./')


            self.files = dict()
            self.files['log'] = config['files']['log']
            self.logger.logger.debug('log file pattern is ' +  self.files['log'])
            logList = glob.glob(self.files['log'])
            if not logList:
                self.logger.logger.error('no log file found.')
                return
            self.log = logList[0]

            #first we just cache all lines
            with open(self.log) as logfile:
                self.loglines = logfile.readlines()

            self.lemonlog = 'lemon_' +  self.log
            with open(self.lemonlog, 'w') as tlog:
                tlog.truncate()

            #important structure: sipmsgs, is a list with order
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
            #NOTE: assume mo means left, mt means right...
            self.callidmapmomt = dict()

            #record ue's num
            self.uenum = ''



        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)


    def findmainlog(self, path):
        pass

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
            self.logger.logger.error('tags is empty')
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
        self.logger.logger.info('data anchor is ' + datalenanchor)
        while dataindex >= 0:
            if datalenanchor not in self.loglines[dataindex]:
                dataindex = dataindex - 1
            else:
                break


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
            for pindex in range(start,end+1):
                sendsip['msg'].append(self.loglines[pindex])
                llog.write(self.loglines[pindex])
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
        self.logger.logger.info('data anchor is ' + datalenanchor)
        while dataindex >= 0:
            if datalenanchor not in self.loglines[dataindex]:
                dataindex = dataindex + 1
            else:
                break

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
            #record req line and other fields here
            for pindex in range(start,end+1):
                recvsip['msg'].append(self.loglines[pindex])
                llog.write(self.loglines[pindex])
        self.sipmsgs.append(recvsip)

    def getFlow(self):
        #rePattern = r'' + 'fsm(.*)' + ' | \[TIMER.*\]' + '|recv.*data' + '| process request' + '|process response'
        lemonpattern = self.getPattern(self.lemontags)
        self.logger.logger.info('lemon pattern is ' + lemonpattern)
        if not lemonpattern:
            self.logger.logger.error('lemonpattern is none!')
            return
        sprdPattern = re.compile(lemonpattern)
        senderpattern = re.compile(r'' + self.sendertags)
        receiverpattern = re.compile(r'' +  self.receivertags)

        self.logger.logger.info("all output will be redirected to " + self.lemonlog)
        with open(self.log) as logfile:
            for lineno, line in enumerate(logfile):
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
            if 'REGISTER' in sip['cseq']:

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


    def assembleDiagStr(self):
        #first define all UE and network name
        elements = dict()
        #add stub for NETWORK
        elements['NETWORK'] = 'NETWORK'
        self.findUE()

        for index, entity in enumerate(self.entities):
            if entity == self.uenum:
                #seqdial's title do not support + char??!!
                elements[self.uenum] = 'UE_' + entity.strip('+')
            else:
                elements[entity] = 'otherUE_' + entity.strip('+')


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
            callid = sip['callid']
            if 'REGISTER' in sip['cseq'] and sip['pasonum']:
                self.logger.logger.info('use P-Associate-URI'+ str(sip['pasonum']) + ' for register ' + sip['fromnum'])
                self.callidmapmomt[callid]['mo'] = sip['pasonum']


        for sipindex, sip in enumerate(self.diagsips):
            callid = sip['callid']

            if sip['send']:
                #NOTE: space is important
                direct = ' -> '
                #find left/right by callid

                leftnum = self.callidmapmomt[callid]['mo']
                rightnum = self.callidmapmomt[callid]['mt']
                left = elements[leftnum]
                right = elements[rightnum]
            else:
                direct = ' <- '
                leftnum = self.callidmapmomt[callid]['mo']
                rightnum = self.callidmapmomt[callid]['mt']
                left = elements[leftnum]
                right = elements[rightnum]


            #some color or string decoration
            # session modificaiton should be marked.
            #TODO: add seperator line for each call process
            sdpstring = ""
            action = ''
            mediadirection = ''
            labelcolor = ""
            notecolor =  ""



            basedirect =  left + direct + right
            label =  " [label = \"" + sip['label'] + "\""

            timestamp = "\"Time: " + sip['timestamp'] + "\n"
            if sip['issdp'] and sip['isinvite'] :
                action = "Note: " +  sip['action'] + '\n'

            if sip['issdp']:
                sdpstring = " with sdp"
                if sip['vdirect']:
                    mediadirection += "video: " + sip['vdirect'] + ','

                if sip['adirect']:
                    mediadirection += 'audio: ' + sip['adirect'] + '\n'

            elif sip['isinvite']:
                sdpstring = " without sdp"
                #B2BUA's request will be marked
                labelcolor = ", color=red"

            cseq = " CSeq: " + sip['cseq'] + sdpstring + '\n'
            #callid = " Call-ID: "+ sip['callid'] + '\n'
            fromtag = " From: " + sip['fromnum'] + '\n'
            totag = " To: " + sip['tonum'] + '\n'
            callid = " Call-ID: " + sip['callid'] + '\n'
            lineno = " log lineno: " + str(sip['lineno']) + "\""

            note = ", note = " + timestamp + cseq + action + mediadirection + fromtag + totag + callid +lineno

            label = label + note + labelcolor + "];\n"
            #print label
            self.diagstr +=  basedirect + label

    def getRealNum(self,string):
        #FIXME: special handling for MESSAGE's deliver report
        # the num may be a address
        if self.sipparser.checkIp(string):
            return 'NETWORK'
        else:
             return string


    def dumpcallidmaping(self):
        for callid,momt in self.callidmapmomt.iteritems():
            self.logger.logger.debug('callid is ' + callid)
            for key,value in momt.iteritems():
                self.logger.logger.debug('key is '+ key + ', value is ' + value)


    def analyzeSdp(self, sip):
        #set default value



        #FIXME: 1. only should scan invite
        #       2. record the same callerid's action flow.
        if sip['sdp']:
            sip['isvideo'] = False
            sip['adirect'] = 'sendrecv'
            sip['vdirect'] = 'sendrecv'
            sipparser = self.sipparser
            for index, sdpline in enumerate(sip['sdp']):
                #1. check media:          m=audio 37042 RTP/AVP 104 0 8 116 103 9 101
                #2. check media redirect: a=sendrecv
                sdppair = sipparser.sdpParser(sdpline)
                if sdppair:
                    type = sdppair['type']
                    value = sdppair['value']
                    if type == 'm':
                        mediadict = sipparser.getmedia(value)
                        if mediadict['mtype'] == 'video':
                            self.logger.logger.debug('found video')
                            sip['isvideo'] = True
                            sip['vport'] = mediadict['mport']
                        else:
                            sip['isvideo'] =  False
                            sip['aport'] = mediadict['mport']

                    elif type == 'a':
                        if sipparser.checksdpDirect(value):
                            #assume that the voice attribute comes first and video later
                            if sip['isvideo'] :
                                self.logger.logger.debug('video direct is ' + value)
                                sip['vdirect'] = value
                            else:
                                sip['adirect'] = value
                                self.logger.logger.debug('audio direct is ' + value)
                    else:
                        #other value.
                        pass

            #now get the conclusion: voice/video/hold/resume

            #FIXME/TODO: should have the sdp nego logic
            if sip['isvideo'] and sip['vport'] != str(0):
                '''
                if sip['vdirect'] == 'sendonly':
                    sip['action'] = 'Hold '
                elif sip['vdirect'] == 'recvonly':
                    sip['action'] = 'Resume '
                elif sip['vdirect'] == 'sendrecv':
                    sip['action'] = 'Start '
                else:
                    sip['action'] = 'Inactive '
                '''
                sip['action'] = 'Video Call'
            else:
                '''
                if sip['adirect'] == 'sendonly':
                    sip['action'] = 'Hold '
                elif sip['adirect'] == 'recvonly':
                    sip['action'] = 'Resume '
                elif sip['adirect'] == 'sendrecv':
                    sip['action'] = 'Start '
                else:
                    sip['action'] = 'Inactive '
                '''
                sip['action'] = 'Voice Call'




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

        for sipindex, sip in enumerate(self.diagsips):

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
            #IMPORTANT: record caller and callee via call-id
            if callid not in self.callidmapmomt:
                #NOTE: here IMPU is set as mo
                if sip['isregister']:
                    momt['mo'] =  self.getRealNum(fromnum)
                    momt['mt'] = 'NETWORK'
                elif sip['issubs']:
                    #NOTIFY, SUBSCRIBE
                    momt['mo'] = self.getRealNum(fromnum)
                    momt['mt'] = 'NETWORK'
                #FIXME: B2BUA's logic not work here, callid is the same
                #elif sip['isinvite'] and sip['issdp'] == False:
                #add special handling for B2BUA's reinvite without sdp
                #   momt['mo'] = 'NETWORK'
                #  momt['mt'] = self.getRealNum(tonum)
                else:

                    if sip['send']:
                        momt['mo'] = self.getRealNum(fromnum)
                        momt['mt'] = self.getRealNum(tonum)
                    else:
                        momt['mo'] = self.getRealNum(tonum)
                        momt['mt'] = self.getRealNum(fromnum)

                self.callidmapmomt[callid] = momt

            #add logic to parser sdp
            self.analyzeSdp(sip)


        #print 'entities num is ' + str(len(self.entities))
        #print 'callid num is ' + str(len(self.callids))
        #dump all the entities
        for index, entity in enumerate(self.entities):
            self.logger.logger.debug('participant_' + str(index) + ' is ' + entity)

        self.dumpcallidmaping()





    def parseFlow(self):
        '''
            generate the diag from self.sipmsgs
        :return:
        '''
        sipparser = self.sipparser
        for index, sipobj in enumerate(self.sipmsgs):
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
            diaginfo['send'] = sipobj['send']
            diaginfo['sdp'] = list()


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
                    self.logger.logger.debug('found status ' + status + ' in ' +  str(index) + ' sip msg')
                    diaginfo['lineno'] = lineno
                    diaginfo['label'] = status
                    diaginfo['timestamp'] = timestamp
                    #self.diagstr += "UE " + direct + " NETWORK [label = \"" + status + " No." + str(lineno)+"\"];\n"
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

                if not diaginfo['pasonum']:
                    pasonum = sipparser.getPasoUri(header)
                    if pasonum:
                        diaginfo['pasonum'] = pasonum
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

        #analyze the trim sip
        self.analyzeSip()
        #dump the trim sip
        self.dumpDiagsip()
        if self.diagsips:
            self.assembleDiagStr()


    def drawLemonDiag(self):
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
        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)
        pngname = self.log.split('.')[0] + '.png'
        draw = drawer.DiagramDraw('PNG', diagram, filename=pngname)
        draw.draw()
        draw.save()
        pass

if __name__ == '__main__':
    fp = flowParser()
    fp.getFlow()
    #fp.drawDemoDiag()
    #fp.parseFlowOld()
    fp.parseFlow()
    fp.drawLemonDiag()
    #print len(fp.sipmsgs)
