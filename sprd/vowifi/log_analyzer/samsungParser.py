# -*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
import sys
import glob
from configobj import ConfigObj,ConfigObjError
import re

from lib.logConf import logConf
from lib.utils import utils
import logging

from seqdiag import parser, builder, drawer

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
            self.keywords['recvrsp'] = config['samsung']['keywords']['recvrsp']
            self.keywords['recvreq'] = config['samsung']['keywords']['recvreq']
            self.keywords['sendreq'] = config['samsung']['keywords']['sendreq']
            self.keywords['sendrsp'] = config['samsung']['keywords']['sendrsp']
            self.keywords['ikemsg'] = config['samsung']['keywords']['ikemsg']


            self.loglevel =  config['logging']['loglevel']

            #have to set loglevel to interger...
            self.logger = logConf(debuglevel=logging.getLevelName(self.loglevel))
            self.utils = utils(configpath='./')

            self.diagstr = ''

            realpath = os.path.realpath(logname)
            self.log = realpath
            self.diagdir = os.path.realpath(os.path.dirname(logname)) + '/'

            #all msgs will be included
            self.msgs = list()

            with open(self.log) as samsungfile:
                self.lines = samsungfile.readlines()


        except (ConfigObjError, IOError) as e:
             print('Could not read "%s": %s' % (configfile, e))

    def getRecvSipReq(self, lineno, line):
        reqpattern = re.compile(self.keywords['recvreq'])
        match = reqpattern.search(line)
        if match:
            method = match.group(1)
            cseq = match.group(2)
            self.logger.logger.info('recv sip req method is ' + str(method) + ', cseq is ' + cseq)

            msg = dict()
            msg['method'] = method
            msg['cseq'] = cseq
            msg['isrecvreq'] = True
            msg['isrecvrsp'] = False
            msg['issendreq'] = False
            msg['issendrsp'] = False
            msg['isike'] = False
            msg['direct'] = '<-'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno

            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                tlog.write(str(lineno) + ' ' + line)


    def getRecvSipRsp(self, lineno, line):
        recvpattern = re.compile(self.keywords['recvrsp'])
        match = recvpattern.search(line)
        if match:
            rspcode = match.group(1)
            cseq = match.group(2)
            self.logger.logger.info('recv sip rsp is ' + str(rspcode) + ', cseq is ' + cseq)

            msg = dict()
            msg['rspcode'] = rspcode
            msg['cseq'] = cseq
            msg['isrecvreq'] = False
            msg['isrecvrsp'] = True
            msg['issendreq'] = False
            msg['issendrsp'] = False
            msg['isike'] = False
            msg['direct'] = '<-'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno

            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                tlog.write(str(lineno) + ' ' + line)

    def getSendSipreq(self, lineno, line):
        sendsippattern = re.compile(self.keywords['sendreq'])
        match = sendsippattern.search(line)
        if match:
            cseqnum = match.group(1)
            method = match.group(2)
            cseq = str(cseqnum) + ' ' + method
            self.logger.logger.info('send sip req method is ' + method + ' , cseq is ' + cseq)

            msg = dict()
            msg['cseq'] = cseq
            msg['method'] = method
            msg['isrecvreq'] = False
            msg['isrecvrsp'] = False
            msg['issendreq'] = True
            msg['issendrsp'] = False
            msg['isike'] = False
            msg['direct'] = '->'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno

            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                tlog.write(str(lineno) + ' ' + line)

    def getSendSipRsp(self, lineno, line):
        sendsiprsppattern =  re.compile(self.keywords['sendrsp'])
        match = sendsiprsppattern.search(line)
        if match:
            rspcode = match.group(1)
            cseq = match.group(2)
            self.logger.logger.info('send sip rsp is ' + str(rspcode) + ', cseq is ' + cseq)

            msg = dict()
            msg['isrecvreq'] = False
            msg['isrecvrsp'] = False
            msg['issendreq'] = False
            msg['issendrsp'] = True
            msg['isike'] = False
            msg['rspcode'] = rspcode
            msg['cseq'] = cseq
            msg['direct'] = '->'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno
            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                tlog.write(str(lineno) + ' ' + line)

    def getIke(self, lineno, line):
        ikepattern = re.compile(self.keywords['ikemsg'])
        match = ikepattern.search(line)
        if match:
            srcip = match.group(1)
            srcport = match.group(2)
            direct = match.group(3)
            dstip = match.group(4)
            dstport = match.group(5)
            msgid = match.group(6)
            msgcontent = match.group(7)
            self.logger.logger.info('srcip ' + srcip + ', srcport is ' + str(srcport) + ', direct is ' + direct
                                    + ' , dstip is ' + dstip + ', dstport is ' + str(dstport) + ', msgid is ' + str(msgid)
                                    + ' ike msg is ' + msgcontent)

            msg = dict()
            msg['isrecvrsp'] = False
            msg['issendreq'] = False
            msg['issendrsp'] = False
            msg['isike'] = True
            msg['direct'] = direct
            msg['msgid'] = msgid
            msg['msgcontent'] = msgcontent
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno



            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                tlog.write(str(lineno) + ' ' + line)


    def assembleDiagStr(self):
        for index, msg in enumerate(self.msgs):
            if msg['isike']:
                #NOTE: two space is important, ' -> ', ' <- '
                basedirect = 'Samsung' + ' ' + msg['direct'] + ' ' + 'NETWORK'

                #strip space and comma
                hint = msg['msgcontent'].strip(' ,')

                label =  " [label = \"IKEv2 Msg: " + hint   + "\" "
                msgid = " MsgId: " + str(msg['msgid']) + '\n'
                content = ' Content: ' + msg['msgcontent'] + '\n'
                timestamp = "Time: " + msg['timestamp'] + "\n"
                lineno = ' LineNo: ' + str(msg['lineno']) + '\n'
                note = ", note = \"" + msgid + content + timestamp + lineno + "\""
                label = label + note + "];\n"
                self.diagstr += basedirect + label
                '''
                Samsung <- NETWORK [label = "IKEv2 Msg: HDR, IDr, EAP
                " , note = " MsgId: 1
                Content: , HDR, IDr, EAP
                Time: 05-02 18:55:17.721
                LineNo: 778
                "];
                '''
            elif msg['issendreq']:
                basedirect = 'Samsung' + ' ' + msg['direct'] + ' ' + 'NETWORK'
                label = " [label = \"Send SIP Request: "  + msg['method'] + "\""
                cseq = ' Cseq: ' + str(msg['cseq']) + '\n'
                method = ' Method: ' + msg['method'] + '\n'
                timestamp = "Time: " + msg['timestamp'] + "\n"
                lineno = ' LineNo: ' + str(msg['lineno']) + '\n'
                note = ", note = \"" + method + cseq + timestamp + lineno + "\""
                label = label + note + "];\n"
                self.diagstr += basedirect + label
                '''
                Samsung -> NETWORK [label = "Send SIP Request: REGISTER", note = " Method: REGISTER
                Cseq: 1 REGISTER
                Time: 05-02 18:55:20.409
                LineNo: 2853
                "];
                '''
            elif msg['issendrsp']:
                basedirect = 'Samsung' + ' ' + msg['direct'] + ' ' + 'NETWORK'
                label = " [label = \"Send SIP Rsp: " + str(msg['rspcode']) + "\""
                cseq = ' Cseq: ' + str(msg['cseq']) + '\n'
                rspcode = ' RspCode: ' + msg['rspcode'] + '\n'
                timestamp = "Time: " + msg['timestamp'] + "\n"
                lineno = ' LineNo: ' + str(msg['lineno']) + '\n'
                note = ", note = \"" + rspcode + cseq + timestamp + lineno + "\""
                label = label + note + "];\n"
                self.diagstr += basedirect + label
                '''
                Samsung <- NETWORK [label = "Recv SIP Rsp: 401", note = " RspCode: 401
                Cseq:  1 REGISTER
                Time: 05-02 18:55:21.849
                LineNo: 4175
                "];
                '''
            elif msg['isrecvreq']:
                basedirect = 'Samsung' + ' ' + msg['direct'] + ' ' + 'NETWORK'
                label = " [label = \"Recv SIP Request: " + msg['method'] + "\""
                cseq = ' Cseq: ' + str(msg['cseq']) + '\n'
                method = ' Method: ' + msg['method'] + '\n'
                timestamp = "Time: " + msg['timestamp'] + "\n"
                lineno = ' LineNo: ' + str(msg['lineno']) + '\n'
                note = ", note = \"" + rspcode + cseq + timestamp + lineno + "\""
                label = label + note + "];\n"
                self.diagstr += basedirect + label
            elif msg['isrecvrsp']:
                basedirect = 'Samsung' + ' ' + msg['direct'] + ' ' + 'NETWORK'

                label = " [label = \"Recv SIP Rsp: " + str(msg['rspcode']) + "\""
                cseq = ' Cseq: ' + str(msg['cseq']) + '\n'
                rspcode = ' RspCode: ' + msg['rspcode'] + '\n'
                timestamp = "Time: " + msg['timestamp'] + "\n"
                lineno = ' LineNo: ' + str(msg['lineno']) + '\n'
                note = ", note = \"" + rspcode + cseq + timestamp + lineno + "\""
                label = label + note + "];\n"
                self.diagstr += basedirect + label
            else:
                self.logger.logger.info('impossible to come here.')

    def drawDiag(self):
        diagram_definition = u"""seqdiag {\n"""
        #Set fontsize.
        diagram_definition += " edge_length = 300;\n  // default value is 192"
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
        basename = os.path.basename(self.log)
        pngname = basename.split('.')[0] + '.png'
        diagname = basename.split('.')[0] + '.diag'

        pngname = self.diagdir + pngname
        diagname = self.diagdir + diagname
        with open(diagname, 'w') as diagfile:
            diagfile.write(diagram_definition)
        #self.utils.setup_imagedraw()
        #self.utils.setup_plugins()
        self.utils.setup_imagedraw()
        self.utils.setup_noderenderers()

        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)

        self.logger.logger.info('diagram file is ' + pngname)
        draw = drawer.DiagramDraw('PNG', diagram, filename=pngname, debug=True)
        draw.draw()
        draw.save()

    def getflow(self):
        #hard code here
        '''
        samsungfileList = glob.glob(self.files['log'])
        if not samsungfileList:
            print 'no samsung log file found.'
            return
        '''

        samsungfile = self.log
        basename = os.path.basename(samsungfile)
        trimname = 'trim_' + basename
        self.trimlog = os.path.dirname(samsungfile) + '/'+ trimname
        with open(self.trimlog, 'w') as tlog:
            tlog.truncate()
        print self.keywords['ikemsg']

        '''
        rePattern = r'' + self.keywords['recv'] + '|' + self.keywords['sendreq'] + '|' + self.keywords['sendrsp'] \
                    + '|' + self.keywords['ikemsg']
        samsungPattern = re.compile(rePattern)
        '''
        print "all output will be redirected to " + self.trimlog
        with open(samsungfile) as sfile:
            for lineno, line in enumerate(sfile):


                self.getIke(lineno, line)
                self.getSendSipreq(lineno, line)
                self.getSendSipRsp(lineno,line)
                self.getRecvSipRsp(lineno, line)
                '''
                if samsungPattern.search(line):
                    with open(self.trimlog, 'a+') as tlog:
                        tlog.write(str(lineno) + ' ' + line)
                '''
        self.assembleDiagStr()
        self.drawDiag()



if __name__ == '__main__':
    print 'start to parse samsung'
    sp = samsungParser(logname='./samsung.log')
    sp.getflow()