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
from blockdiag.utils.bootstrap import create_fontmap
from PyPDF2 import PdfFileMerger, PdfFileReader

path = os.path.dirname(os.path.realpath(__file__))

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
            self.logtags = config['samsung']['pattern']['logtags']


            #TODO: add a state machine
            self.keywords['statechange'] = config['samsung']['keywords']['statechange']
            self.keywords['wifichange'] = config['samsung']['keywords']['wifichange']
            self.keywords['wfcchange'] = config['samsung']['keywords']['wfcchange']

            self.loglevel =  config['logging']['loglevel']

            #have to set loglevel to interger...
            self.logger = logConf(debuglevel=logging.getLevelName(self.loglevel))
            self.utils = utils(configpath='./')

            self.diagstr = ''

            realpath = os.path.realpath(logname)
            self.log = realpath
            self.diagdir = os.path.realpath(os.path.dirname(logname)) + '/'
            self.diagtempdir = self.diagdir + 'temp/'
            #first of all, create the tempdir
            self.utils.mkdirp(self.diagtempdir)

            #all msgs will be included
            self.msgs = list()

            self.lines = list()

            #will split the msg into list
            self.diagstrList = None
            self.pdfList = list()
            self.splitgate = 40

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
            msg['isevent'] = False
            msg['isike'] = False
            msg['direct'] = '<-'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno

            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                line = line.replace('\r', '')
                tlog.write(str(lineno) + ' ' + line)
            return True
        else:
            return False


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
            msg['isevent'] = False
            msg['direct'] = '<-'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno

            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                line = line.replace('\r', '')
                tlog.write(str(lineno) + ' ' + line)
            return True
        else:
            return False

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
            msg['isevent'] = False
            msg['direct'] = '->'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno

            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                line = line.replace('\r', '')
                tlog.write(str(lineno) + ' ' + line)
            return True
        else:
            return False

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
            msg['isevent'] = False
            msg['rspcode'] = rspcode
            msg['cseq'] = cseq
            msg['direct'] = '->'
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            msg['timestamp'] = timestamp
            msg['lineno'] = lineno
            self.msgs.append(msg)

            with open(self.trimlog, 'a+') as tlog:
                line = line.replace('\r', '')
                tlog.write(str(lineno) + ' ' + line)
            return True
        else:
            return False

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
                line = line.replace('\r', '')
                tlog.write(str(lineno) + ' ' + line)
            return True
        else:
            return False


    def assembleDiagStr(self):

        splitnum = len(self.msgs) / int(self.splitgate) + 1
        self.logger.logger.info('the diagsips will be divided into %d ' % splitnum)
        self.diagstrList = [''] * splitnum
        for index, msg in enumerate(self.msgs):

            sector = (index + 1) / int(self.splitgate)

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
                onestr = basedirect + label
                self.diagstr += onestr
                self.diagstrList[sector] += onestr
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
                onestr = basedirect + label
                self.diagstr += onestr
                self.diagstrList[sector] += onestr
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
                onestr = basedirect + label
                self.diagstr += onestr
                self.diagstrList[sector] += onestr
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
                onestr = basedirect + label
                self.diagstr += onestr
                self.diagstrList[sector] += onestr
            elif msg['isrecvrsp']:
                basedirect = 'Samsung' + ' ' + msg['direct'] + ' ' + 'NETWORK'

                label = " [label = \"Recv SIP Rsp: " + str(msg['rspcode']) + "\""
                cseq = ' Cseq: ' + str(msg['cseq']) + '\n'
                rspcode = ' RspCode: ' + msg['rspcode'] + '\n'
                timestamp = "Time: " + msg['timestamp'] + "\n"
                lineno = ' LineNo: ' + str(msg['lineno']) + '\n'
                note = ", note = \"" + rspcode + cseq + timestamp + lineno + "\""
                label = label + note + "];\n"
                onestr = basedirect + label
                self.diagstr += onestr
                self.diagstrList[sector] += onestr
            elif msg['isevent']:
                #wifi, wfc, handover event comes here.
                onestr = msg['content']
                self.diagstr += onestr
                self.diagstrList[sector] += onestr
            else:
                self.logger.logger.info('impossible to come here.')
    def drawAllDiag(self):
        estimatetime = 0.1 * int(len(self.msgs))
        self.logger.logger.info('length of all msgs is ' + str(len(self.msgs)) + ' may take ' + str(estimatetime) + ' seconds')


        for index, diagstr in enumerate(self.diagstrList):
            self.drawOneDiag(diagstr, index)

        #do the merge.
        merger = PdfFileMerger()
        for index, filename in enumerate(self.pdfList):
            merger.append(PdfFileReader(file(filename, 'rb')))

        basename = os.path.basename(self.log)
        #samsung's main log name there will be more than one dot
        dotlength = basename.split('.')

        finalpdfname = self.diagdir + ''.join(dotlength) + '.pdf'
        merger.write(finalpdfname)

    def drawOneDiag(self, diagstr, postfix):
        diagram_definition = u"""seqdiag {\n"""
        #Set fontsize.
        diagram_definition += " edge_length = 300;\n  // default value is 192"
        diagram_definition += "default_fontsize = 30;\n"
        #Do not show activity line
        diagram_definition += "activation = none;\n"
        #Numbering edges automaticaly
        diagram_definition +="autonumber = True;\n"
        diagram_definition += diagstr
        diagram_definition += u""" }\n"""
        # generate the diag string and draw it
        #self.logger.logger.info('seqdiag is ' + diagram_definition)
        #write the diagram string to file
        basename = os.path.basename(self.log)
        pngname = basename.split('.')[0] + '_' + str(postfix) + '.png'
        diagname = basename.split('.')[0] + '_' + str(postfix) +'.diag'

        pngname = self.diagtempdir + pngname
        diagname = self.diagtempdir + diagname
        pdfname = self.diagtempdir + basename.split('.')[0]+ '_' + str(postfix) + '.pdf'
        self.pdfList.append(pdfname)
        with open(diagname, 'w') as diagfile:
            diagfile.write(diagram_definition)
        #self.utils.setup_imagedraw()
        #self.utils.setup_plugins()
        self.utils.setup_imagedraw()
        self.utils.setup_noderenderers()

        tree = parser.parse_string(diagram_definition)
        diagram = builder.ScreenNodeBuilder.build(tree)

        self.logger.logger.info('diagram file is ' + pngname)
        options = dict()
        options['fontmap'] = ''
        options['font'] = list()
        options['font'].append(path + '/font/DejaVuSerif.ttf:1')
        options = utils.dotdict(options)
        fm = create_fontmap(options)
        pdfdraw = drawer.DiagramDraw('PDF', diagram, filename=pdfname, debug=True, fontmap=fm)
        pdfdraw.draw()
        pdfdraw.save()
        '''
        png is not used here
        draw = drawer.DiagramDraw('PNG', diagram, filename=pngname, debug=True)
        draw.draw()
        draw.save()
        '''

    def checkwifi(self, lineno, line):

        wifipattern = re.compile(self.keywords['wifichange'])
        match = wifipattern.search(line)
        if match:
            string = match.group(1).strip()
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            self.logger.logger.error('string is ' +  string)
            seperateline = ' === ' + string + ' time: ' + str(timestamp) + '=== \n'
            msg = dict()
            msg['isevent'] = True
            msg['isrecvreq'] = False
            msg['isrecvrsp'] = False
            msg['issendreq'] = False
            msg['issendrsp'] = False
            msg['isike'] = False
            msg['content'] = seperateline
            self.msgs.append(msg)
            return True
        else:
            return False


    def checkwfc(self, lineno, line):
        wfcpattern = re.compile(self.keywords['wfcchange'])
        match = wfcpattern.search(line)
        if match:
            string = match.group(1).strip()
            self.logger.logger.error('string is ' +  string)
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            seperateline = ' === ' + string + ' time: ' + str(timestamp) + '=== \n'
            msg = dict()
            msg['isevent'] = True
            msg['isrecvreq'] = False
            msg['isrecvrsp'] = False
            msg['issendreq'] = False
            msg['issendrsp'] = False
            msg['isike'] = False
            msg['content'] = seperateline
            self.msgs.append(msg)
            return True
        else:
            return False

    def checkhostate(self, lineno, line):
        hostatepattern = re.compile(self.keywords['statechange'])
        match = hostatepattern.search(line)
        if match:
            fromstate = match.group(1)
            tostate = match.group(2)
            string = "From " + fromstate + ' handover to ' + tostate
            self.logger.logger.error('string is ' +  string)
            fields = line.split(' ')
            timestamp = fields[0] + ' ' + fields[1]
            seperateline = ' === ' + string + ' time: ' + str(timestamp) + '=== \n'
            msg = dict()
            msg['isevent'] = True
            msg['isrecvreq'] = False
            msg['isrecvrsp'] = False
            msg['issendreq'] = False
            msg['issendrsp'] = False
            msg['isike'] = False
            msg['content'] = seperateline
            self.msgs.append(msg)
            return True
        else:
            return False

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

        alllogtags = self.utils.getPattern(self.logtags)
        alllogpattern = re.compile(alllogtags)

        print "all output will be redirected to " + self.trimlog
        with open(samsungfile, 'rb') as sfile:
            self.lines = sfile.readlines()
            for lineno, line  in enumerate(self.lines):

                handled = False
                #self.logger.logger.info('lineno is ' + str(lineno) + '  '+line)
                handled = self.checkwifi(lineno, line)

                if not handled:
                    handled = self.checkwfc(lineno, line)
                else:
                    continue
                if not handled:
                    handled = self.checkhostate(lineno, line)
                else:
                    continue

                if not handled:
                    handled = self.getIke(lineno, line)
                else:
                    continue

                if not handled:
                    handled = self.getSendSipreq(lineno, line)
                else:
                    continue
                if not handled:
                    handled = self.getSendSipRsp(lineno,line)
                else:
                    continue
                if not handled:
                    handled = self.getRecvSipRsp(lineno, line)
                if not handled:
                    handled =  self.getRecvSipReq(lineno, line)
                else:
                    continue

                if not handled:
                    if alllogpattern.search(line):
                        with open(self.trimlog, 'a+') as tlog:
                            line = line.replace('\r', '')
                            tlog.write(str(lineno) + ' ' + line)
                '''
                if samsungPattern.search(line):
                    with open(self.trimlog, 'a+') as tlog:
                        tlog.write(str(lineno) + ' ' + line)
                '''
        self.assembleDiagStr()
        self.drawAllDiag()



if __name__ == '__main__':
    print 'start to parse samsung'
    sp = samsungParser(logname='./samsung.log')
    sp.getflow()
    #wifistring = "EPDG -- [EPDGService](  986): Wifi is disconnected"
    #sp.checkwifi(12,wifistring)