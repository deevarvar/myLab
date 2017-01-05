#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com


import os
import sys
import re
from lib.logConf import logConf
from configobj import ConfigObj,ConfigObjError
from datetime import datetime
#Note: AT> will have a rsp: AT< OK, if not OK we will display it.

from seqdiag import parser, builder, drawer
from blockdiag.utils.bootstrap import create_fontmap
from PyPDF2 import PdfFileMerger, PdfFileReader
from lib.utils import utils


path = os.path.dirname(os.path.realpath(__file__))

class radioParser():
    def __init__(self, logname, outputdir = './'):
        try:
            configfile = path + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.radiolog = logname
            self.config = config
            self.pattern = dict()
            self.pattern['pdnpattern'] = config['radioParser']['pdnpattern']
            self.pattern['hopattern'] = config['radioParser']['hopattern']
            self.pattern['wifienpattern'] = config['radioParser']['wifienpattern']
            #self.pattern['repregpattern'] = config['radioParser']['repregpattern']
            #self.pattern['qryregpattern'] = config['radioParser']['qryregpattern']
            self.pattern['regstspattern'] = config['radioParser']['regstspattern']
            self.pattern['attachpattern'] = config['radioParser']['attachpattern']
            self.pattern['vowfregpattern'] = config['radioParser']['vowfregpattern']
            self.pattern['wifiinfopattern'] = config['radioParser']['wifiinfopattern']
            self.pattern['lteinfopattern'] = config['radioParser']['lteinfopattern']
            self.pattern['callendpattern'] = config['radioParser']['callendpattern']
            #self.pattern['errorpattern'] = config['radioParser']['errorpattern']
            self.pattern['updatedrpattern'] = config['radioParser']['updatedrpattern']
            self.pattern['rtppattern'] = config['radioParser']['rtppattern']
            self.pattern['volteimspattern'] = config['radioParser']['volteimspattern']
            self.pattern['volteregaddrpattern'] = config['radioParser']['volteregaddrpattern']

            #there are always dirty msgs to ignroe, Orz...
            self.ignoremsg = list()
            self.ignoremsg.append("VoLTE Unregistered")

            self.initkeypattern()
            self.atmsgs = list()
            self.logger = logConf()

            #diagstr
            self.diagstr = ''

            #will split the msg into list
            self.diagstrList = None
            self.pdfList = list()
            self.splitgate = 30

            self.utils = utils(configpath='./')
            prefix = outputdir

            self.utils.createdirs(outputdir)
            self.diagdir = prefix + '/diagrams/'
            self.diagdirdiag = prefix + '/diagrams/diag/'
            self.diagdirpdf = prefix + '/diagrams/pdf/'
            self.logdir = prefix + '/logs/'

            realpath = os.path.realpath(logname)
            basename = os.path.basename(realpath)
            self.trimlog = self.logdir + 'trim_' + basename
            with open(self.trimlog, 'w') as tlog:
                tlog.truncate()

            self.starttime = datetime.now()

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)

    def initkeypattern(self):
        #define the pattern and pattern helper
        self.keypattern = list()
        pdnpattern = dict()
        pdnpattern['pattern'] = re.compile(self.pattern['pdnpattern'])
        pdnpattern['func'] = self.getPdnstate
        pdnpattern['direct'] = '<-'
        self.keypattern.append(pdnpattern)

        wifienpattern = dict()
        wifienpattern['pattern'] = re.compile(self.pattern['wifienpattern'])
        wifienpattern['func'] = self.getWifiEnable
        wifienpattern['direct'] = '->'
        self.keypattern.append(wifienpattern)


        hopattern = dict()
        hopattern['pattern'] = re.compile(self.pattern['hopattern'])
        hopattern['func'] = self.getHOstate
        hopattern['direct'] = '->'
        self.keypattern.append(hopattern)

        '''
        qryregpattern = dict()
        qryregpattern['pattern'] = re.compile(self.pattern['qryregpattern'])
        qryregpattern['func'] = self.getqrystring
        qryregpattern['direct'] = '->'
        self.keypattern.append(qryregpattern)
        '''

        regstspattern = dict()
        regstspattern['pattern'] = re.compile(self.pattern['regstspattern'])
        regstspattern['func'] = self.getregstate
        regstspattern['direct'] = '<-'
        self.keypattern.append(regstspattern)

        attachpattern = dict()
        attachpattern['pattern'] = re.compile(self.pattern['attachpattern'])
        attachpattern['func'] = self.getattachstate
        attachpattern['direct'] = '->'
        self.keypattern.append(attachpattern)

        vowfregpattern = dict()
        vowfregpattern['pattern'] = re.compile(self.pattern['vowfregpattern'])
        vowfregpattern['func'] = self.getwifireg
        vowfregpattern['direct'] = '->'
        self.keypattern.append(vowfregpattern)

        wifiinfopattern = dict()
        wifiinfopattern['pattern'] = re.compile(self.pattern['wifiinfopattern'])
        wifiinfopattern['func'] = self.getwifiinfo
        wifiinfopattern['direct'] = '->'
        self.keypattern.append(wifiinfopattern)

        lteinfopattern = dict()
        lteinfopattern['pattern'] = re.compile(self.pattern['lteinfopattern'])
        lteinfopattern['func'] = self.getlteinfo
        lteinfopattern['direct'] = '<-'
        self.keypattern.append(lteinfopattern)

        callendpattern = dict()
        callendpattern['pattern'] = re.compile(self.pattern['callendpattern'])
        callendpattern['func'] = self.getcallendstring
        callendpattern['direct'] = '->'
        self.keypattern.append(callendpattern)

        '''
        #seems cp logs always have CME error... Orz
        errorpattern = dict()
        errorpattern['pattern'] = re.compile(self.pattern['errorpattern'])
        errorpattern['func'] = self.geterror
        errorpattern['direct'] = '<-'
        self.keypattern.append(errorpattern)
        '''
        updatedrpattern = dict()
        updatedrpattern['pattern'] = re.compile(self.pattern['updatedrpattern'])
        updatedrpattern['func'] = self.getupdatedr
        updatedrpattern['direct'] = '->'
        self.keypattern.append(updatedrpattern)

        rtppattern = dict()
        rtppattern['pattern'] = re.compile(self.pattern['rtppattern'])
        rtppattern['func'] = self.getrtp
        rtppattern['direct'] = '<-'
        self.keypattern.append(rtppattern)

        volteimspattern = dict()
        volteimspattern['pattern'] = re.compile(self.pattern['volteimspattern'])
        volteimspattern['func'] = self.imsenable
        volteimspattern['direct'] = '->'
        self.keypattern.append(volteimspattern)

        volteregaddrpattern = dict()
        volteregaddrpattern['pattern'] = re.compile(self.pattern['volteregaddrpattern'])
        volteregaddrpattern['func'] = self.getvolteaddr
        volteregaddrpattern['direct'] = '<-'
        self.keypattern.append(volteregaddrpattern)

    def initAtmsg(self, line):
        #common steps
        #add timestamp and atcmd
        atmsg = dict()
        #get timestamp first
        fields = line.strip().split(' ')
        #04-17 23:21:24.420
        timestamp = fields[0] + ' ' + fields[1]
        atmsg['timestamp'] = timestamp
        atmsg['issip'] = 0
        atmsg['isat'] = 1
        return atmsg

    def getPdnstate(self, state):
        if state == '1':
            return "PDN connection established"
        elif state == '2':
            return "PDN connection request"
        elif state == '0':
            return "Deactivate PDN connection"
        else:
            return "Unknow PDN state"

    #sample function
    def getPdnAtMsg(self, pattern, line):
        match = pattern.search(line)
        if match:
            self.logger.logger.debug(line)
            atmsg = self.initAtmsg(line)
            atmsg['atcmd'] = match.group(0).strip().replace('"', '')
            pdnstate = match.group(1).strip()
            atmsg['action'] = self.getPdnstate(pdnstate)
            self.logger.logger.debug('pdn state is %s, action is %s' % (pdnstate, atmsg['action']))
            self.atmsgs.append(atmsg)
            return True
        else:
            return False


    def getWifiEnable(self, state):
        if state == '1':
            return "Vowifi Available"
        elif state == '0':
            return "Vowifi Unavailable"
        else:
            return "Unknow Vowifi Enable state"

    def getHOstate(self, state):
        if state == '1':
            return "IDLE handover to VoWifi"
        elif state == '2':
            return "IDLE handover to VoLte"
        elif state == '3':
            return "Handover to VoWifi in Call"
        elif state == '4':
            return "Handover to VoLte in Call"
        else:
            return "Unknown Handover state"

    def getregstate(self, state):
        if state == '0':
            return "VoLTE Unregistered"
        elif state == '1':
            return "VoLTE Registered"
        else:
            return "Unknown VoLTE Register state"

    def getattachstate(self,state):
        if state == '0':
            return "EPDG failed to attach"
        elif state == '1':
            return "EPDG attach successfully"
        else:
            state = "Unknown attach status"
    def getqrystring(self):
        return "Query CP Regsiter state"

    def getcallendstring(self):
        return "Vowifi Call End"

    def getupdatedr(self):
        return "Update Data Router"

    def getwifireg(self, state):
        if state == '0':
            return "VoWiFi failed to Register"
        elif state == '1':
            return "VoWiFi Registered successfully"
        else:
            state = "Unknown VoWiFi Register state"

    def getwifiinfo(self, info):
        #"405872003c00000ec"
        #strip "
        return "wifi info: " + info.replace('"', '')

    def getlteinfo(self, info):

        return "lte info: " + info.replace('"', '')

    def geterror(self, error):
        if error == '3':
            return "Error: operation not allowed"
        else:
            return "Error Code: " + error

    def getrtp(self, state):
        if state == '0':
            return "receive RTP data"
        elif state == '1':
            return "No RTP data!"
        elif state == '2':
            return "Clear RTP state"
        else:
            return "Unknow RTP state"

    def imsenable(self):
        return "Enable VoLTE IMS"

    def getvolteaddr(self, addr):
        return "Volte Register Addr is \n" + addr

    def getAtmsg(self,keypattern, line, lineno):
        '''
        :param pattern:  all kinds of pattern
        :param line:
        :param actionfunc: used to get the match.group(1) 's action
        :return:  True/False , get or not
        '''
        pattern = keypattern['pattern']
        actionfunc = keypattern['func']
        direct = keypattern['direct']
        match = pattern.search(line)
        if match:
            #self.logger.logger.debug(line)
            with open(self.trimlog, 'a+') as tlog:
                tlog.write(line)

            atmsg = self.initAtmsg(line)
            #replace double quote, or seqdiag will fail!
            atmsg['atcmd'] = match.group(0).strip().replace('"', '')
            atmsg['direct'] = direct
            atmsg['lineno'] = 'radio log:' + str(lineno)

            groupnum = pattern.groups
            if not actionfunc:
                atmsg['action'] = ''
            else:
                if groupnum >= 1:
                    state = match.group(1).strip()
                else:
                    state = ''

                if not state:
                    atmsg['action'] = actionfunc()
                else:
                    atmsg['action'] = actionfunc(state)

                self.logger.logger.debug('state is %s, action is %s' % (state, atmsg['action']))

            #only if the msg is not to be ignored...
            for i,ignore in enumerate(self.ignoremsg):
                if ignore == atmsg['action']:
                    self.logger.logger.info('atcmd %s , action is %s ignored...' % (atmsg['atcmd'], atmsg['action']))
                    return False

            self.atmsgs.append(atmsg)
            return True
        else:
            return False

    def dumpatmsgs(self):
        for index, atmsg in enumerate(self.atmsgs):
            self.logger.logger.info('atmsg index is ' + str(index) )
            for key, value in atmsg.iteritems():
                self.logger.logger.info('key is ' + key  + ', value is ' + str(value))

    def drawAllDiag(self):
        estimatetime = 0.1 * int(len(self.atmsgs))
        self.logger.logger.info('length of all msgs is ' + str(len(self.atmsgs)) + ' may take ' + str(estimatetime) + ' seconds')

        for index, diagstr in enumerate(self.diagstrList):
            self.drawOneDiag(diagstr, index)

        #do the merge.
        merger = PdfFileMerger()
        for filename in self.pdfList:
            merger.append(PdfFileReader(file(filename, 'rb')))

        basename = os.path.basename(self.radiolog)
        finalpdfname = self.diagdir + basename.split('.')[0] + '.pdf'
        merger.write(finalpdfname)
        self.endtime = datetime.now()
        self.duration = self.endtime - self.starttime
        self.logger.logger.info('length of all msgs is ' + str(len(self.atmsgs)) + '  takes ' + str(self.duration) + ' seconds')
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


        elementstr = "UE; CP;"
        diagram_definition +=elementstr + '\n'
        diagram_definition += '\n'

        diagram_definition += diagstr
        diagram_definition += u""" }\n"""
        # generate the diag string and draw it
        #self.logger.logger.info('seqdiag is ' + diagram_definition)
        #write the diagram string to file
        basename = os.path.basename(self.radiolog)
        #print self.diagdirdiag + '\n'
        diagname = self.diagdirdiag + basename.split('.')[0] + '_' + str(postfix) + '.diag'
        #print diagname + '\n'
        pdfname = self.diagdirpdf + basename.split('.')[0] + '_' + str(postfix) + '.pdf'

        self.pdfList.append(pdfname)
        print diagram_definition
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



    def getflow(self):

        #init patterns
        with open(self.radiolog, 'rb') as rfile:
            for lineno, line in enumerate(rfile):
                for index, keypattern in enumerate(self.keypattern):
                    self.getAtmsg(keypattern,line, lineno)
        self.dumpatmsgs()
        return self.atmsgs

    #assemblestr only used in this file
    #for other module, only asseble is used in other module.
    def assembleStr(self):
        splitnum = len(self.atmsgs) / int(self.splitgate) + 1
        self.logger.logger.info('the atmsgs will be divided into %d ' % splitnum)
        self.diagstrList = [''] * splitnum
        for index,atmsg in enumerate(self.atmsgs):
            sector = (index + 1) / int(self.splitgate)
            basedirect = 'UE' + ' ' + atmsg['direct'] + ' '+ 'CP'
            #only need label, note
            label =  " [label = \"" + atmsg['action']  + "\" "
            atcmd = " AtCmd: " + atmsg['atcmd'] + '\n'
            timestamp = " time: " + atmsg['timestamp'] + '\n'
            lineno = "Lineno: " + atmsg['lineno'] + '\n'
            note = ", note = \"" + atcmd + timestamp + lineno+ "\""
            label = label + note + "];\n"
            onestr = basedirect + label
            self.diagstr += onestr
            self.diagstrList[sector] += onestr


if __name__ == '__main__':
    rp = radioParser(logname='./0-radio-07-27-11-29-56.log')
    #rp = radioParser(logname='./0-radio-07-27-11-13-22.log')

    #rp = radioParser(logname='./0-radio-07-14-11-19-19.log')

    #rp = radioParser(logname='./0-radio-07-14-12-11-19.log')
    rp.getflow()
    rp.assembleStr()
    rp.drawAllDiag()