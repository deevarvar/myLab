#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
#record important event

import re
import json
import os
import sys
import re

from configobj import ConfigObj,ConfigObjError

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('./')
from logConf import logConf
import logging
from sprdErrCode import *
from collections import Counter
from reportHelper import *
from operator import itemgetter

class Msglevel():
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

#define some event types: user, phone, scenarioes
class ReportType():
    USEREVENT_BASE = 0x1000
    PHONEEVENT_BASE = 0x2000
    SCEEVENT_BASE = 0x3000

#TODO: add detailed event description: process, result


class ReportEvent():
    def __init__(self, configpath='..', reportpath=None):
        try:
            configfile = configpath + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.reportpath = reportpath
            self.logger = logConf()

            #error event need to be marked red
            #use Msglevel.ERROR to indicate
            self.errorevent = list()

            #record every report, the Raw Data
            self.reportlist = list()

            #event table, processed data
            #three kinds of tables:
            # 1. useraction: wfc, wifi,
            # 2. phone:      s2b, reg, ho
            # 3. scenario :  call/sms
            self.usertable = dict()
            self.usertable['list'] = list()
            self.usertable['name'] = "usertable"
            self.usertable['title'] = "User Action"

            self.phonetable = dict()
            self.phonetable['list'] = list()
            self.phonetable['name'] = "phonetable"
            self.phonetable['title'] = "Phone Status"

            self.scenariotable = dict()
            self.scenariotable['list'] = list()
            self.scenariotable['name'] = "scenariotable"
            self.scenariotable['title'] = "VoWiFi Service"

            self.etable = dict()
            self.etable['list'] = list()
            self.etable['name'] = "etable"
            self.etable['title'] = "All Event"

            self.tableattr = dict()
            #for event table
            self.tableattr['etable'] = dict()
            self.tableattr['etable']['caption'] = "Event table"
            self.tableattr['etable']['thlist'] = ["No.", "Event name", "Occurence", 'Details']

            #each error detail should have a different format

            self.tableattr['errtable'] = dict()
            #this caption should be overwritten
            self.tableattr['errtable']['caption'] = "Error table"
            self.tableattr['errtable']['thlist'] = ["No.", "Timestamp","Error Code", 'lineno', 'line']
            self.tableattr['errtable']['tname'] = ""
            self.htmlstr = ''

            self.errorcount = 0

            with open(self.reportpath, 'w') as rlog:
                rlog.truncate()


        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configpath + '/config.ini', e)

    #some getter function for eventtable attribute
    def getEventTableCaption(self):
        return self.tableattr['etable']['caption']
    def getEventTableThlist(self):
        return self.tableattr['etable']['thlist']


    def setEventTlist(self, list):
        self.etable['list'] = list

    def getEventTlist(self):
        return self.etable['list']

    def getEventTname(self):
        return self.etable['name']

    def getEventTitle(self):
        return self.etable['title']

    def getUserTlist(self):
        return self.usertable['list']

    def getUserTname(self):
        return self.usertable['name']

    def getUserTitle(self):
        return self.usertable['title']

    def getPhoneTlist(self):
        return self.phonetable['list']

    def getPhoneTname(self):
        return self.phonetable['name']

    def getPhoneTitle(self):
        return self.phonetable['title']

    def getScenarioTlist(self):
        return self.scenariotable['list']

    def getScenarioTname(self):
        return self.scenariotable['name']

    def getScenarioTitle(self):
        return self.scenariotable['title']


    def getErrorIndex(self, index):
        return "#Error_" + str(index)
    def getErrorId(self, index):
        return "Error_" + str(index)

    def isValidTable(self, table):
        if type(table) is list and len(table) > 0 :
            return True
        else:
            return False

    def genEventTable(self, onereport, table):
        #each report will be added into the table

        ename = onereport['event']
        errorstr = onereport['errorstr']

        #check the eventname, if not exist, then added, if exist, count plus
        if name_in_list(ename, 'ename', table):
            updatereportEvent(onereport, table)
        else:
            newevent = constructreportEvent(onereport)
            table.append(newevent)

    def genEventDetails(self,errorlist):
        detailstr = ''
        if type(errorlist) is list and len(errorlist) > 0:
            for index, error in enumerate(errorlist):
                count = str(error['errorcount'])
                estr = error['errorstr']
                detailstr += estr + ': ' + count + ' Times<br>'

        return detailstr


    def fillReport(self, msg):
        #simply grep event by types:
        #1. user action: wifi conn/discon, wfc enabled/disabled, airplane
        #2. phone action: attach, reg, ho
        #3. scenario: call, conf, sms , etc

        #just to parse the report type.
        if type(msg) is dict and msg and 'report' in msg:
            report = msg['report']
            if report and 'type' in report:
                rtype = report['type']
                if rtype and int(rtype) >= ReportType.USEREVENT_BASE:
                    if type(report['event']) is str:
                        report['timestamp'] = msg['timestamp']
                        report['line'] = msg['line']
                        report['lineno'] = msg['lineno']
                        self.reportlist.append(report)
                        #add function to generate the event overview

                        #the report structure is
                        '''
                        {
                           'event':
                           'errorstr':
                           'timestamp':
                           'line':
                           'lineno':
                        }
                        '''
                        event = report['event'].strip('\n')
                        #record error event
                        if report['level'] == Msglevel.ERROR:
                            self.errorevent.append(event)

                        #there will three kinds of tables
                        if rtype == ReportType.USEREVENT_BASE:
                            self.genEventTable(report, self.getUserTlist())
                        elif rtype == ReportType.PHONEEVENT_BASE:
                            self.genEventTable(report, self.getPhoneTlist())
                        elif rtype == ReportType.SCEEVENT_BASE:
                            self.genEventTable(report, self.getScenarioTlist())


    def genheaderopen(self):
        headeropenstr = ''
        headeropenstr += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN http://www.w3.org/TR/html4/loose.dtd\">\n"
        headeropenstr += "<html><head>"
        headeropenstr += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n"
        headeropenstr += "<style type=\"text/css\">\n"
        headeropenstr += "table {border-collapse: collapse;}\n"
        headeropenstr += "td {padding: 0px;text-align: center;}\n"
        headeropenstr += "</style></head><body>\n"
        return headeropenstr

    def genheaderclose(self):
        headerclosestr = ""
        headerclosestr += "</body>"
        headerclosestr += "</html>\n"
        return headerclosestr



    def gentableopen(self, caption, columnlist, tname):
        tableopenstr = ""
        if type(columnlist) is list and columnlist:
            tableopenstr += "<table border=\"1\">\n"
            tableopenstr += "<caption id=\"" + tname +"\"><b>" + caption + "</b></caption>"
            for index, column in enumerate(columnlist):
                tableopenstr +="<th>" + column +"</th>"
        return tableopenstr

    def genrowopen(self):
        rowopenstr = ""
        rowopenstr +="<tr>\n"
        return rowopenstr

    def gencolumn(self, content):
        #column color will be detemined internally
        bgcolor = "white"
        if content in self.errorevent:
            bgcolor = "red"

        columnstr = ""
        columnstr += "<td style=\"background-color:" + bgcolor + "\">" + content + "</td>"
        return columnstr

    def genrowclose(self):
        rowclosestr = ""
        rowclosestr += "</tr>"
        return rowclosestr

    def gentableclose(self):
        tableclosestr = ""
        tableclosestr += "</table><br>\n"
        return tableclosestr

    def genulopen(self):
        ulstr = "<ul>"
        return ulstr

    def genulclose(self):
        ulstr = "</ul>\n"
        return ulstr

    def genli(self, content):
        listr = ""
        listr += "<li>" + content + "</li>\n"
        return listr

    def genaref(self,content, href):
        arefstr = ""
        arefstr += "<a href=\""+ href +"\">" + content + "</a>\n"
        return arefstr

    def genOverviewIndex(self):
        overviewstr = ''
        overviewstr += self.genulopen()
        listr1 = self.genli("Event Overview")
        username = self.getUserTname()
        phonename = self.getPhoneTname()
        scenarioname = self.getScenarioTname()
        overviewstr += self.genaref(listr1, username)
        overviewstr += self.genulopen()
        #FIXME

        userlistr = self.genli(self.getUserTitle())
        #add the id
        overviewstr += self.genaref(userlistr, '#' + username)

        phonelistr = self.genli(self.getPhoneTitle())
        #add the id
        overviewstr += self.genaref(phonelistr, '#' + phonename)

        scenariolistr = self.genli(self.getScenarioTitle())
        #add the id
        overviewstr += self.genaref(scenariolistr, '#' + scenarioname)


        overviewstr += self.genulclose()

        return overviewstr

    def generateIndex(self):
        #parse the etable, generate the index and sub index
        indexstr = ""


        indexstr += self.genOverviewIndex()
        #if no error , the li is not used;
        #but for sprd, there will be always error.
        listr2 = self.genli("Error Scenarioes")
        indexstr += self.genaref(listr2, "")

        etable = self.getEventTlist()
        indexstr += self.genulopen()
        for index, eventdict in enumerate(etable):
            event = eventdict['ename']
            if event in self.errorevent:
                listr = self.genli(event)
                indexstr += self.genaref(listr, self.getErrorIndex(index))

        indexstr += self.genulclose()

        return indexstr

    def genTitle(self, id, string):
        title = ''
        title += '<h2 id=\''+ str(id) + '\'>'+ string + '</h2>'
        return title

    def genOneTableHTML(self, table, tabletitle,tableid):

        #get eventlist and iterate it, wirte it in right place
        testcaption = self.getEventTableCaption()
        thlist = self.getEventTableThlist()

        tablehtml = ''
        tablehtml += self.genTitle(tableid, tabletitle)
        tablehtml += self.gentableopen(testcaption, thlist, tableid)

        self.logger.logger.info('DEBUG----------------')
        self.logger.logger.info(table)
        for index, eventdict in enumerate(table):
             event = eventdict['ename']
             count = str(eventdict['enamecount'])
             detailstr = self.genEventDetails(eventdict['errorlist'])
             tablehtml +=self.genrowopen()
             tablehtml +=self.gencolumn(str(index+1))
             tablehtml +=self.gencolumn(event)
             tablehtml +=self.gencolumn(count)
             tablehtml +=self.gencolumn(detailstr)
             tablehtml +=self.genrowclose()
        tablehtml +=self.gentableclose()
        tablehtml += self.genhorizonline()
        return tablehtml

    def generateAllTableHTML(self):


        etablehtml = ""
        etablehtml += self.genOneTableHTML(self.getUserTlist(), tabletitle=self.getUserTitle(), tableid=self.getUserTname())
        etablehtml += self.genOneTableHTML(self.getPhoneTlist(), tabletitle=self.getPhoneTitle(), tableid=self.getPhoneTname())
        etablehtml += self.genOneTableHTML(self.getScenarioTlist(), tabletitle=self.getScenarioTitle(), tableid=self.getScenarioTname())
        return etablehtml

    def genhorizonline(self):
        return "<hr>\n"

    def genOneErrorTable(self, dlist, index):
        errortablehtml = ''
        caption = self.tableattr['errtable']['caption']
        thlist = self.tableattr['errtable']['thlist']
        tname = str(index)

        errortablehtml += self.gentableopen(caption, thlist, tname)
        #["No.", "Timestamp","Error Code", 'lineno']
        for i, error in enumerate(dlist):
            no = i
            timestamp = error['timestamp']
            errorstr = error['errorstr']
            lineno = str(error['lineno'])
            line = str(error['line'])
            errortablehtml += self.genrowopen()
            errortablehtml +=self.gencolumn(str(no+1))
            errortablehtml +=self.gencolumn(timestamp)
            errortablehtml +=self.gencolumn(errorstr)
            errortablehtml +=self.gencolumn(lineno)
            errortablehtml +=self.gencolumn(line)
            errortablehtml += self.genrowclose()

        errortablehtml += self.gentableclose()
        #add horizon line
        errortablehtml += self.genhorizonline()

        return errortablehtml

    def genAllErrorTable(self):

        allerrortable = ''
        etable = self.getEventTlist()

        for index, eventdict in enumerate(etable):
            event = eventdict['ename']
            detaillist = eventdict['errordetailslist']
            etableid =  self.getErrorId(index)

            if event in self.errorevent:
                #generate one error table
                allerrortable += self.genTitle(etableid, event)
                allerrortable += self.genOneErrorTable(detaillist, etableid)
        return allerrortable


    def generateHTML(self):
        #first of all, combine all tables
        etable = self.getEventTlist()
        usertable = self.getUserTlist()
        phonetable = self.getPhoneTlist()
        scenariotable = self.getScenarioTlist()

        etable = usertable + phonetable + scenariotable

        if self.isValidTable(etable) > 0 :
            #sort the output by occurence descending
            usertable = sorted(usertable, key=itemgetter('enamecount'),  reverse=True)
            phonetable = sorted(phonetable, key=itemgetter('enamecount'),  reverse=True)
            scenariotable = sorted(scenariotable, key=itemgetter('enamecount'),  reverse=True)
            etable = sorted(etable, key=itemgetter('enamecount'),  reverse=True)
            self.setEventTlist(etable)
            self.htmlstr += self.genheaderopen()
            self.htmlstr += self.generateIndex()
            self.htmlstr += self.generateAllTableHTML()
            self.htmlstr += self.genAllErrorTable()
            self.htmlstr += self.genheaderclose()
            with open(self.reportpath, 'a+') as rlog:
                rlog.write(self.htmlstr)



    def cloudpic(self):
        # yuntu which will demonstrate the relationship between modules
        pass
