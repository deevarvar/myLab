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

#add user defined lib
sys.path.append('./lib')
from SipParser import SipParser

path = os.path.dirname(os.path.realpath(__file__))



class flowParser():
    def __init__(self):
        try:
            configfile = path + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.lemontags = config['sprd']['lemontags']
            self.servicetags = config['sprd']['servicetags']
            self.adaptertags = config['sprd']['adaptertags']
            self.sendertags = config['sprd']['sendertags']
            self.receivertags =  config['sprd']['receivertags']
            self.siptags = config['sprd']['siptags']

            self.files = dict()
            self.files['log'] = config['files']['log']
            print self.files['log']
            logList = glob.glob(self.files['log'])
            if not logList:
                print 'no log file found.'
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

            self.sipparser = SipParser(configpath='./')

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

    def getSendSip(self,line,lineno):
        senddatalen =  self.getSendLen(line)
        if not senddatalen:
            print 'no recv data len in line ' + str(lineno)
            return

        #search backward
        found = 0
        index = lineno - 1

        while index >= 0:
            if self.siptags in self.loglines[index]:
                found +=1
                print 'found send siptags in ' + str(index) + ', found num is ' + str(found)
                if found == 1:
                    end =  index
                    index = index - 1
                else:
                    start = index
                    #record the timestamp
                    fields = self.loglines[index].split(' ')
                    #04-17 23:21:24.420
                    timestamp = fields[0] + ' ' + fields[1]
                    break
            else:
                index = index - 1
        with open(self.lemonlog, 'a+') as llog:
            print start, end
            sendsip = dict()
            sendsip['send'] = True
            sendsip['lineno'] = lineno
            sendsip['timestamp'] = timestamp
            sendsip['msg'] = list()
            for pindex in range(start+1,end):
                sendsip['msg'].append(self.loglines[pindex])
                llog.write(self.loglines[pindex])
        self.sipmsgs.append(sendsip)


    def getRecvSip(self,line, lineno):
        recvdatalen = self.getRecvLen(line)
        if not recvdatalen:
            print 'no recv data len in line ' + str(lineno)
            return
        #search forward
        #we have to search two siptags and write the lines between the two tags
        found = 0
        index = lineno + 1

        while index <=  len(self.loglines):
            if self.siptags in self.loglines[index]:
                found += 1
                print 'found recv siptags in ' + str(index) + ', found num is ' + str(found)
                if found == 1:
                    start = index
                    index += 1
                else:
                    end = index
                    #record the timestamp
                    fields = self.loglines[index].split(' ')
                    #04-17 23:21:24.420
                    timestamp = fields[0] + ' ' + fields[1]
                    #if we found two siptags then break
                    break
            else:
                index += 1
        with open(self.lemonlog, 'a+') as llog:
            print start, end
            recvsip = dict()
            recvsip['send'] = False
            recvsip['msg'] = list()
            recvsip['lineno'] = lineno
            recvsip['timestamp'] = timestamp
            #record req line and other fields here
            for pindex in range(start+1,end):
                recvsip['msg'].append(self.loglines[pindex])
                llog.write(self.loglines[pindex])
        self.sipmsgs.append(recvsip)

    def getFlow(self):
        #rePattern = r'' + 'fsm(.*)' + ' | \[TIMER.*\]' + '|recv.*data' + '| process request' + '|process response'
        lemonpattern = self.getPattern(self.lemontags)
        print 'lemon pattern is ' + lemonpattern
        if not lemonpattern:
            print 'lemonpattern is none!'
            return
        sprdPattern = re.compile(lemonpattern)
        senderpattern = re.compile(r'' + self.sendertags)
        receiverpattern = re.compile(r'' +  self.receivertags)

        print "all output will be redirected to " + self.lemonlog
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
            print 'receiving non-SIP msg, len is ' + str(recvdatalen)
            return None
        else:
            return recvdatalen


    def getSendLen(self, line):
        #get length
        sendpattern = r'.*send data\[(.*)\].*to.*'
        senddatalen = self.getDataLen(sendpattern, line)
        #FIXME: the 250 is some kind of exp value
        if senddatalen < 250:
            print 'send non-SIP msg , len is ' + str(senddatalen)
            return  None
        else:
            return senddatalen

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
        line = self.lemonlines[lineno]
        recvdatalen = self.getRecvLen(line)

        if not recvdatalen:
            print 'no recv data len in line' + str(lineno)
            return

        #start to search forward
        start = lineno+1
        requesttags = "process request"
        responsetags = "process response"

        while start <= len(self.lemonlines):
            waterline = self.lemonlines[start]
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

        line = self.lemonlines[lineno]
        senddatalen = self.getSendLen(line)
        if not senddatalen:
            print 'no send data len in line' + str(lineno)
            return
        #start to search backward
        start = lineno - 1
        while start >= 0:
            waterline = self.lemonlines[start]
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
            print 'request index is ' + str(sipindex)
            for key,value in sip.iteritems():
                print str(key) + ':' + str(value)

    def assembleDiagStrOld(self,diaginfo):
        #sample UE -> NETWORK [label = "200 OK", note = "Cseq 1 REGISTER\n lineno: 888"];
        if diaginfo['send']:
            direct = '->'
        else:
            direct = '<-'

        #TODO: UE and NETWORK maybe need to change
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
            if sip['isregister']:
                #TODO: identify REGISTER
                # use cseq:.*REGISTER to tell
                print 'start to probe the REGISTER msg'
                pass

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
            print 'ue name is '+ elements[self.uenum]


        #1. element order
        #2. get the UE's number
        #
        left = ''
        right = ''
        direct = ''

        for sipindex, sip in enumerate(self.diagsips):
            #TODO: add logic to check REGISTER
            callid = sip['callid']
            if sip['isregister']:
                #TODO: identify REGISTER
                # use cseq:.*REGISTER to tell
                print 'need to probe the REGISTER msg'
                pass
            else:
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

            basedirect =  left + direct + right
            label =  " [label = \"" + sip['label'] + "\""

            timestamp = "\"time: " + sip['timestamp'] + "\n"
            cseq = " CSeq: " + sip['cseq'] + '\n'
            callid = " Call-ID: "+ sip['callid'] + '\n'
            lineno = " lineno: " + str(sip['lineno']) + "\""

            note = ", note = " + timestamp + cseq + callid+ lineno

            label = label + note + "];\n"
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
            print 'callid is ' + callid
            for key,value in momt.iteritems():
                print 'key is '+ key + ', value is ' + value


    def analyzeSip(self):
        #get all UE's phone number,
        #check if reinivte does not have sdp

        #rules are listed below:
        # 1. only invite has 'fromnum', 'tonum'
        # 2. use call-id to identify the caller/callee
        # 3. TODO: MESSAGE should be parsed
        # 4: SUBSCRIBE/NOTIFY
        # 5: REGISTER
        for sipindex, sip in enumerate(self.diagsips):

            fromnum = sip['fromnum']
            tonum = sip['tonum']
            callid = sip['callid']

            if self.sipparser.checkIp(fromnum) == False:
                if fromnum not in self.entities:
                    self.entities.append(fromnum)
            if self.sipparser.checkIp(tonum) == False:
                if tonum not in self.entities:
                    self.entities.append(tonum)
            momt = dict()
            #IMPORTANT: record caller and callee via call-id
            if callid not in self.callidmapmomt:
                if sip['send']:
                    #FIXME: need to add register logic
                    momt['mo'] = self.getRealNum(fromnum)
                    momt['mt'] = self.getRealNum(tonum)
                else:
                    momt['mo'] = self.getRealNum(tonum)
                    momt['mt'] = self.getRealNum(fromnum)

                self.callidmapmomt[callid] = momt


        #print 'entities num is ' + str(len(self.entities))
        #print 'callid num is ' + str(len(self.callids))
        #dump all the entities
        for index, entity in enumerate(self.entities):
            print entity

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
            diaginfo['issubs'] = False
            diaginfo['send'] = sipobj['send']
            for msgindex,header in enumerate(sip):
                #get reqeust line/status line, other header

                method = sipparser.getMethod(header)
                if method:
                    print 'found method ' + method  + ' in ' + str(index) + ' sip msg'
                    diaginfo['lineno'] = lineno
                    diaginfo['label'] =  method
                    diaginfo['timestamp'] = timestamp
                    #if method is INVITE/OPTIONS/UPDATE/INFO/REFER/MESSAGE, check Call-ID and From, to
                    if method == 'INVITE' or method == 'OPTIONS' or method == 'UPDATE' \
                            or method == 'INFO' or method == 'REFER' or method == 'MESSAGE':
                        diaginfo['isinvite'] = True
                        continue

                    if method == 'REGISTER' :
                        diaginfo['isregister'] = True
                        continue

                    if method == 'SUBSCRIBE' or method == 'NOTIFY' or method == 'PUBLISH':
                        diaginfo['issubs'] = True
                        continue

                if 'callid' not in diaginfo:
                    callid = sipparser.getHeaderContent(header, 'Call-ID')
                    if callid:
                        diaginfo['callid'] = callid

                if 'from' not in diaginfo:
                    fromtag = sipparser.getHeaderContent(header, 'From')
                    if fromtag:
                        diaginfo['from'] = fromtag
                        num = sipparser.getNumber(fromtag)
                        diaginfo['fromnum'] = num

                if 'to' not in diaginfo:
                    totag = sipparser.getHeaderContent(header, 'To')
                    if totag:
                        diaginfo['to'] = totag
                        num = sipparser.getNumber(totag)
                        diaginfo['tonum'] = num


                cseq = sipparser.getCSeq(header)
                if cseq:
                    print 'found cseq ' + cseq  + ' in ' + str(index) + ' sip msg'
                    diaginfo['cseq'] = cseq
                    continue

                status = sipparser.getStatusLine(header)
                if status:
                    print 'found status ' + status + ' in ' +  str(index) + ' sip msg'
                    diaginfo['lineno'] = lineno
                    diaginfo['label'] = status
                    diaginfo['timestamp'] = timestamp
                    #self.diagstr += "UE " + direct + " NETWORK [label = \"" + status + " No." + str(lineno)+"\"];\n"
                    continue

            #add function to construct the diagram string
            self.diagsips.append(diaginfo)
            #oboselete logic
            #if diaginfo:
                #self.assembleDiagStrOld(diaginfo)
        #dump the trim sip
        self.dumpDiagsip()
        #analyze the trim sip
        self.analyzeSip()
        if self.diagsips:
            self.assembleDiagStr()


    def drawLemonDiag(self):
        diagram_definition = u"""seqdiag {\n"""

        diagram_definition += self.diagstr
        diagram_definition += u""" }\n"""
        # generate the diag string and draw it
        print diagram_definition
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
