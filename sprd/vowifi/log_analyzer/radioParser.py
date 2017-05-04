#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

#should add color for at cmd and add report in final html
#the function is in self.reportevent.fillReport in flowParser.py


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

from lib.sprdErrCode import *
from lib.reportEvent import *
from lib.reportConverter import *
from lib.constants import * #we need Q850map

path = os.path.dirname(os.path.realpath(__file__))

#define class to build action
class actionBuilder():
    def __init__(self):
        self.eventname = ''
        self.color = "black"
        self.msglevel = Msglevel.INFO

        self.report = dict()
        self.report['type'] = None
        self.report['event'] = None
        self.report['level'] = Msglevel.INFO
        self.report['errorstr'] = None
        self.report['lineno'] = None
        self.report['line'] =  None
        self.report['timestamp'] = None


    def setEventName(self, name):
        if name:
            self.eventname = name
        else:
            self.eventname = ''

    def setMsglevel(self, level):
        if level:
            self.msglevel = level
        else:
            self.msglevel = Msglevel.INFO

    def setColor(self, color):
        if color:
            self.color = color
        else:
            self.color = 'black'

    def setColorByLevel(self, level):
        if self.color == "black":
            color = maplevel2color(level)
            self.color = color

    def setReport(self, report):
        if report:
            self.report = report

    def setAll(self, eventname, msglevel, color):
        self.setEventName(eventname)
        self.setMsglevel(msglevel)
        self.setColor(color)
        self.setColorByLevel(msglevel)


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
            self.pattern['repregpattern'] = config['radioParser']['repregpattern']
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

            #srvcc pattern
            self.pattern['querysrvccpattern'] = config['radioParser']['querysrvccpattern']
            self.pattern['qresultsrvccpattern'] = config['radioParser']['qresultsrvccpattern']

            self.pattern['setsrvccpattern'] = config['radioParser']['setsrvccpattern']

            self.pattern['setsrvccreportpattern'] = config['radioParser']['setsrvccreportpattern']
            self.pattern['querysrvccreportpattern'] = config['radioParser']['querysrvccreportpattern']

            self.pattern['qresultsrvccreportpattern'] = config['radioParser']['qresultsrvccreportpattern']

            self.pattern['srvcchoinfopattern'] = config['radioParser']['srvcchoinfopattern']
            self.pattern['callinfosyncpattern'] = config['radioParser']['callinfosyncpattern']
            self.pattern['networksrvccpattern'] = config['radioParser']['networksrvccpattern']

            self.pattern['mestatepattern'] = config['radioParser']['mestatepattern']
            self.pattern['horegupdatepattern'] = config['radioParser']['horegupdatepattern']
            self.pattern['appcscfpattern'] = config['radioParser']['appcscfpattern']

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

        repregpattern = dict()
        repregpattern['pattern'] = re.compile(self.pattern['repregpattern'])
        repregpattern['func'] = self.repregstate
        repregpattern['direct'] = '<-'
        self.keypattern.append(repregpattern)

        '''
        regstspattern = dict()
        regstspattern['pattern'] = re.compile(self.pattern['regstspattern'])
        regstspattern['func'] = self.getregstate
        regstspattern['direct'] = '<-'
        self.keypattern.append(regstspattern)
        '''

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

        #add srvcc part
        querysrvccpattern = dict()
        querysrvccpattern['pattern'] = re.compile(self.pattern['querysrvccpattern'])
        querysrvccpattern['func'] = self.querysrvcc
        querysrvccpattern['direct'] = '->'
        self.keypattern.append(querysrvccpattern)

        qresultsrvccpattern = dict()
        qresultsrvccpattern['pattern'] = re.compile(self.pattern['qresultsrvccpattern'])
        qresultsrvccpattern['func'] = self.querysrvccresult
        qresultsrvccpattern['direct'] = '<-'
        self.keypattern.append(qresultsrvccpattern)

        setsrvccpattern = dict()
        setsrvccpattern['pattern'] = re.compile(self.pattern['setsrvccpattern'])
        setsrvccpattern['func'] = self.setsrvcc
        setsrvccpattern['direct'] = '->'
        self.keypattern.append(setsrvccpattern)

        setsrvccreportpattern = dict()
        setsrvccreportpattern['pattern'] = re.compile(self.pattern['setsrvccreportpattern'])
        setsrvccreportpattern['func'] = self.setsrvccreport
        setsrvccreportpattern['direct'] = '->'
        self.keypattern.append(setsrvccreportpattern)

        querysrvccreportpattern = dict()
        querysrvccreportpattern['pattern'] = re.compile(self.pattern['querysrvccreportpattern'])
        querysrvccreportpattern['func'] = self.qsrvccreport
        querysrvccreportpattern['direct'] = '->'
        self.keypattern.append(querysrvccreportpattern)

        qresultsrvccreportpattern = dict()
        qresultsrvccreportpattern['pattern'] = re.compile(self.pattern['qresultsrvccreportpattern'])
        qresultsrvccreportpattern['func'] = self.qsrvccreportresult
        qresultsrvccreportpattern['direct'] = '<-'
        self.keypattern.append(qresultsrvccreportpattern)

        srvcchoinfopattern = dict()
        srvcchoinfopattern['pattern'] = re.compile(self.pattern['srvcchoinfopattern'])
        srvcchoinfopattern['func'] = self.srvcchoinfo
        srvcchoinfopattern['direct'] = '<-'
        self.keypattern.append(srvcchoinfopattern)

        networksrvccpattern = dict()
        networksrvccpattern['pattern'] = re.compile(self.pattern['networksrvccpattern'])
        networksrvccpattern['func'] = self.networksrvcc
        networksrvccpattern['direct'] = '<-'
        self.keypattern.append(networksrvccpattern)

        callinfosyncpattern = dict()
        callinfosyncpattern['pattern'] = re.compile(self.pattern['callinfosyncpattern'])
        callinfosyncpattern['func'] = self.callinfosync
        callinfosyncpattern['direct'] = '->'
        self.keypattern.append(callinfosyncpattern)

        mestatepattern = dict()
        mestatepattern['pattern'] = re.compile(self.pattern['mestatepattern'])
        mestatepattern['func'] = self.mestate
        mestatepattern['direct'] = '<-'
        self.keypattern.append(mestatepattern)


        horegupdatepattern = dict()
        horegupdatepattern['pattern'] = re.compile(self.pattern['horegupdatepattern'])
        horegupdatepattern['func'] = self.horegupdate
        horegupdatepattern['direct'] = '<-'
        self.keypattern.append(horegupdatepattern)


        appcscfpattern = dict()
        appcscfpattern['pattern'] = re.compile(self.pattern['appcscfpattern'])
        appcscfpattern['func'] = self.setappcscf
        appcscfpattern['direct'] = '->'
        self.keypattern.append(appcscfpattern)


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
        '''
        atmsg['action'] should be a dict
        member should be eventname, color, msglevel
        '''
        atmsg['action'] = actionBuilder()
        atmsg['report'] = None

        return atmsg

    def getPdnstate(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        if state == '1':
            eventname =  "PDN connection established"
            color = 'green'
            msglevel =  Msglevel.NORMAL
        elif state == '2':
            eventname =  "PDN connection request"
        elif state == '0':
            eventname =  "Deactivate PDN connection"
            color = 'brown'
            msglevel =  Msglevel.WARNING
        else:
            eventname = "Unknow PDN state"
            msglevel = Msglevel.WARNING

        event = mapzhphrase(eventname, ReportCpphrase)
        action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)
        action.setAll(eventname, msglevel,color)
        return action

    def getWifiEnable(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()

        if state == '1':
            eventname =  "Vowifi Available"
            color = 'green'
        elif state == '0':
            eventname = "Vowifi Unavailable"
            msglevel =  Msglevel.ERROR

        else:
            eventname = "Unknow Vowifi Enable state"
            msglevel =  Msglevel.WARNING

        action.setAll(eventname, msglevel,color)

        return action


    def getHOstate(self, state):
        eventname = ''
        color = 'blue'
        msglevel = Msglevel.INFO
        action = actionBuilder()

        if state == '1':
            eventname = "IDLE handover to VoWifi"
        elif state == '2':
            eventname = "IDLE handover to VoLte"
        elif state == '3':
            eventname = "Handover to VoWifi in Call"
        elif state == '4':
            eventname = "Handover to VoLte in Call"

        else:
            eventname = "Unknown Handover state"
            msglevel = Msglevel.WARNING

        action.setAll(eventname, msglevel,color)
        return action

    def repregstate(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()

        if state == '0':
            eventname = "VoLTE Unregistered"
            color = 'brown'
            msglevel = Msglevel.WARNING
            event = mapzhphrase(eventname, ReportCpphrase)
            action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)
        elif state == '1':
            eventname = "VoLTE Registered"
            color = 'green'
            msglevel = Msglevel.NORMAL
            event = mapzhphrase(eventname, ReportCpphrase)
            action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)
        elif state == '2':
            eventname =  "VoLTE Registering"
        elif state == '3':
            eventname = "VoLTE Register fail"
            msglevel = Msglevel.ERROR
            color = 'red'
            event = mapzhphrase(eventname, ReportCpphrase)
            action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)
        elif state == '4':
            eventname =  "Unknow state"
        elif state == '5':
            eventname = "VoLTE Roaming"
        elif state == '6':
            eventname = "VoLTE De-Registering"
            color = 'brown'
            msglevel = Msglevel.WARNING
            event = mapzhphrase(eventname, ReportCpphrase)
            action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)
        else:
            eventname =  "Unknown VoLTE Register state"

        action.setAll(eventname, msglevel,color)
        return action

    def getregstate(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()

        if state == '0':
            eventname =  "VoLTE Unregistered"
            color = 'brown'
        elif state == '1':
            eventname = "VoLTE Registered"
            color = 'green'
        else:
            eventname = "Unknown VoLTE Register state"
            msglevel = Msglevel.WARNING

        action.setAll(eventname, msglevel, color)
        return action

    def getattachstate(self,state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()

        if state == '0':
            eventname = "EPDG failed to attach"
            color = 'red'
            msglevel = Msglevel.ERROR
        elif state == '1':
            eventname = "EPDG attach successfully"
            color = 'green'
        else:
            eventname = "Unknown attach status"
            msglevel = Msglevel.WARNING

        action.setAll(eventname, msglevel, color)
        return action

    def getqrystring(self):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        eventname  = "Query CP Regsiter state"
        action.setAll(eventname, msglevel, color)
        return action

    def getcallendstring(self, calltype):
        eventname = ''
        color = 'brown'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        if calltype == '1':
            callstr = "VoWiFi"
        else:
            callstr = "VoLTE"

        eventname  = callstr + " Call End"
        action.setAll(eventname, msglevel, color)
        return action

    def getupdatedr(self):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        eventname  = "Update Data Router"
        action.setAll(eventname, msglevel, color)
        return action

    def getwifireg(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        if state == '0':
            eventname = "VoWiFi failed to Register"
            color = 'red'
            msglevel = Msglevel.ERROR
        elif state == '1':
            eventname = "VoWiFi Registered successfully"
            color = 'green'
        else:
            eventname = "Unknown VoWiFi Register state"
        action.setAll(eventname, msglevel, color)
        return action

    def getwifiinfo(self, info):
        #"405872003c00000ec"
        #strip "
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        eventname  = "wifi info: " + info.replace('"', '')
        action.setAll(eventname, msglevel, color)
        return action

    def getlteinfo(self, info):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        eventname  = "lte info: " + info.replace('"', '')
        action.setAll(eventname, msglevel, color)
        return action

    def geterror(self, error):
        eventname = ''
        color = 'red'
        msglevel = Msglevel.ERROR
        action = actionBuilder()
        if error == '3':
            eventname = "Error: operation not allowed"
        else:
            eventname =  "Error Code: " + error
        action.setAll(eventname, msglevel, color)
        return action

    def getrtp(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        if state == '0':
            eventname = "receive RTP data"
        elif state == '1':
            eventname = "No RTP data!"
            color = 'red'
            msglevel = Msglevel.ERROR
            event = mapzhphrase(eventname, ReportCpphrase)
            action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)
        elif state == '2':
            eventname = "Clear RTP state"
        else:
            eventname = "Unknow RTP state"
            msglevel = Msglevel.WARNING
        action.setAll(eventname, msglevel, color)
        return action


    def imsenable(self):
        eventname = ''
        color = 'blue'
        action = actionBuilder()
        eventname  = "Enable VoLTE IMS"
        msglevel = Msglevel.WARNING
        event = mapzhphrase(eventname, ReportCpphrase)
        action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)
        action.setAll(eventname, msglevel, color)
        return action

    def getvolteaddr(self, addr):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        eventname = "Volte Register Addr is \n" + addr
        action.setAll(eventname, msglevel, color)
        return action

    def querysrvcc(self):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        eventname  = "Query SRVCC ability"
        action.setAll(eventname, msglevel, color)
        return action


    def querysrvccresult(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()

        state = state.strip()
        if state == "1":
            eventname = "SRVCC Supported"
        elif state == "0":
            eventname = "Unsupported SRVCC"
            color = 'brown'
        else:
            eventname = "Unknown state about SRVCC ability"
            msglevel = Msglevel.WARNING

        action.setAll(eventname, msglevel, color)
        return action

    def setsrvcc(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()

        state = state.strip()
        if state == "1":
            eventname = "Enable SRVCC"
        elif state == "0":
            eventname = "Disable SRVCC"
            color = 'brown'
        else:
            eventname = "Unknown set option about SRVCC ability"
            msglevel = Msglevel.WARNING

        action.setAll(eventname, msglevel, color)
        return action

    def setsrvccreport(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        state = state.strip()
        if state == "1":
            eventname = "Enable SRVCC report"
        elif state == "0":
            eventname = "Disable SRVCC report"
        else:
            eventname = "Unknown set option about SRVCC report"
        action.setAll(eventname, msglevel, color)
        return action

    def qsrvccreport(self):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        eventname = "Query SRVCC report ability"
        action.setAll(eventname, msglevel, color)
        return action

    def qsrvccreportresult(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        state = state.strip()
        if state == "1":
            eventname = "SRVCC report ability"
        elif state == "0":
            eventname = "no SRVCC report ability"
        else:
            eventname = "Unknown set option about SRVCC report ability"
        action.setAll(eventname, msglevel, color)
        return action

    def networksrvcc(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        state = state.strip()
        if state == '1':
            eventname = "Network Support SRVCC"
        else:
            eventname = "Network Do not support SRVCC"
            color = 'brown'
        action.setAll(eventname, msglevel, color)
        return action


    def srvcchoinfo(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        state = state.strip()
        if state == "0":
            eventname = "PS to CS SRVCC Started"
            color = 'brown'
            msglevel = Msglevel.WARNING
        elif state == "1":
            eventname = "PS to CS SRVCC Successfully"
            msglevel = Msglevel.NORMAL
            color = 'green'
        elif state == "2":
            eventname = "PS to CS SRVCC Cancelled"
            color = 'red'
            msglevel = Msglevel.ERROR
        elif state == "3":
            eventname = "PS to CS SRVCC Failed"
            msglevel = Msglevel.ERROR
            color = 'red'
        else:
            eventname = "Unknown state when PS to CS SRVCC"

        event = mapzhphrase(eventname, ReportCpphrase)
        action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)

        action.setAll(eventname, msglevel, color)
        return action

    def callinfosync(self, string):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.WARNING
        action = actionBuilder()
        basestr = "Sync Call Info:\n"
        finalstr = ''

        #<infx>: string, "< call_id >,< dir >,< call_state >,< hold_state >,< mpty_state >, < mpty_order >,
        #< call_type >,< num_type >,< num_str >"
        #do not care about the multiple party, so 1,2,3,4,7,8,9 is needed
        string = string.replace('"', '')
        fields = string.split(',')
        callid = fields[0]
        direct = fields[1]
        callstate = fields[2]
        holdstate = fields[3]
        calltype = fields[6]
        numtype = fields[7]
        num = fields[8]

        callidstr =  "CallId: " + str(callid) + '\n'

        directstr = ''
        if direct == '0':
            directstr = 'MO Call '
        else:
            directstr = 'MT Call '

        callstatestr = ''
        if callstate == '0':
            callstatestr = 'Idle '
        elif callstate == '1':
            callstatestr = 'Dialing '
        elif callstate == '2':
            callstatestr = 'Outgoing '
        elif callstate == '3':
            callstatestr = 'Active'
        elif callstate == '4':
            callstatestr = "Incoming "
        elif callstate == '5':
            callstatestr = "Accept "
        elif callstate == '6':
            callstatestr = "Modify Pending "
        elif callstate == '7':
            callstatestr = "Release "
        elif callstate == '8':
            callstatestr = "CCBS Recall "
        elif callstate == '9':
            callstatestr = "MT wait for rsp "

        holdstatestr = ''
        if holdstate == '2':
            holdstatestr = ",Hold"

        calltypestr = ''
        if calltype == '0':
            calltypestr = 'Normal '
        elif calltype == '1':
            calltypestr = 'Emergency '
        elif calltype == '2':
            calltypestr = 'Video '

        numtypestr = ''
        if numtype == '1':
            numtypestr = 'International '
        elif numtype == '2':
            numtypestr = "National "
        elif numtype == '3':
            numtypestr = "Network "


        #callstr = numtypestr + calltypestr + directstr
        callstr = directstr
        finalstr =  basestr + num + ',' + callstr + ',' +  callstatestr + holdstatestr
        eventname = finalstr

        event = mapzhphrase(eventname, ReportCpphrase)
        action.report = constructReport(type=ReportType.CPEVENT_BASE, event=event, level=msglevel)

        color = 'brown'
        action.setAll(eventname, msglevel, color)
        return action

    def mestate(self, string):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        #<id>,<dir>,<stat>,<type>,<mpty>,<number>,<num_type>,[<bs_type>][,cause]
        string = string.strip()
        fields = string.split(',')
        calldir = fields[1]
        callstat = fields[2]
        calltype = fields[3]
        number = fields[5]
        cause = ''
        if len(fields) >= 8:
            cause = fields[8]

        #useless
        calldirstr = ''
        if calldir == '0':
            calldirstr = "user Initiated"
        else:
            calldirstr = "User Hung up"

        calltypestr = ''
        if calltype == '0':
            calltypestr = 'Voice Call'
        else:
            calltypestr = "CS Data Call"


        callstatstr = 'CallState: '
        if  callstat == '0':
            callstatstr += 'Active'
        elif callstat == '1':
            callstatstr += 'Hang up'
        elif callstat == '2':
            callstatstr += 'Dialing'
        elif callstat == '3':
            callstatstr += 'Alerting'
        elif callstat == '4':
            callstatstr += 'Incoming'
        elif callstat == '5':
            callstatstr += "Waiting"
        elif callstat == '6':
            callstatstr += 'Stop'

        numberstr = "No: " + number
        causestr = ''
        if cause:
            causestr = "Cause: " + getQ850isdn(cause)
        eventname = calltypestr + '\n' + callstatstr + '\n' + numberstr + '\n' + causestr

        action.setAll(eventname, msglevel, color)
        return action

    def horegupdate(self, state):
        eventname = ''
        color = 'black'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        state = state.strip()
        if state == "1":
            #reged , need not report
            return
        elif state == "4":
            eventname = "VoLTE Re-Register Successfully"
            msglevel = Msglevel.NORMAL
            color = 'green'
        elif state == "5":
            eventname = "VoLTE Re-Register Failed"
            msglevel = Msglevel.ERROR
            color = 'red'
        action.setAll(eventname, msglevel, color)
        return action

    def setappcscf(self, setcmd):
        eventname = ''
        color = 'blue'
        msglevel = Msglevel.INFO
        action = actionBuilder()
        setcmdlist = setcmd.strip().split(',')
        if len(setcmdlist) >= 2:
            ptype = setcmdlist[0]
            ip = setcmdlist[1].strip('"')
            eventname = "Set PCSCF Address: \n" + ip
            action.setAll(eventname, msglevel, color)
            return action
        else:
            return None

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
            atmsg['line'] = line.strip(' \t')
            groupnum = pattern.groups
            if actionfunc:
                if groupnum >= 1:
                    state = match.group(1).strip()
                else:
                    state = ''

                if not state:
                    atmsg['action'] = actionfunc()
                else:
                    atmsg['action'] = actionfunc(state)
                if not atmsg['action']:
                    return False

                eventname = atmsg['action'].eventname
                atmsg['report'] = atmsg['action'].report
                self.logger.logger.debug('state is %s, action is %s' % (state, eventname))

            #only if the msg is not to be ignored...
            for i,ignore in enumerate(self.ignoremsg):
                eventname = atmsg['action'].eventname
                if ignore == eventname:
                    self.logger.logger.info('atcmd %s , action is %s ignored...' % (atmsg['atcmd'], eventname))
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
            #only need label, note,
            #add label color
            eventname = atmsg['action'].eventname
            color = atmsg['action'].color

            label =  " [label = \"" + eventname  + "\" "
            labelcolor = ", color=" + color
            atcmd = " AtCmd: " + atmsg['atcmd'] + '\n'
            timestamp = " time: " + atmsg['timestamp'] + '\n'
            lineno = "Lineno: " + atmsg['lineno'] + '\n'
            note = ", note = \"" + atcmd + timestamp + lineno+ "\""

            #AP -> UE [label = "Module: Phone:
            #VoWiFi RegState Update to LOGINED", color = blue,note = " log lineno: 36364
            #Time: 12-26 13:20:08.074"];

            label = label + labelcolor + note + "];\n"
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