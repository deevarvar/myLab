#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import sys
import os
#sys.path.append('./')
#print sys.path
import definition
from config import *
from lib.logConf import logConf
from lib.logutils import logutils
from helper.processmap import *
from helper.excelhelper import *
import re

#TODO list:
#1. find pid by words
#1.1 pid may change, process restart
#2. unittest
#3. decode flow
#3.1 idea is different from old style:
#     media only need the process, simple is beautiful.
#     record start
#     record statistics, pps, sps,rtp
#     record end
# for phrase one:
#      1. log grep
#      2. data statistics
#


class mflow:
    def __init__(self, logname='', outdir='./', loglevel='DEBUG'):
        self.log = os.path.realpath(logname)
        with open(self.log, 'rb') as logfile:
            self.loglines = logfile.readlines()
        self.logger = logConf(debuglevel=loglevel)
        self.logger.logger.info('init flow')
        self.config = config()
        self.logutils = logutils()

        #output is in one extra dir
        self.outdir = os.path.dirname(logname) + '/output'
        self.logutils.mkdirp(self.outdir)

        self.trimlog = self.outdir + '/' + 'media_verbose.log'
        with open(self.trimlog, 'a+')as trimlog:
            trimlog.truncate()

        self.excel = self.outdir + '/' + 'statictics.xlsx'

        #final eventmsg should be processed
        self.eventmsgs = list()

        #pid should be a verbose list
        self.pids = list()

        #call list
        self.calllist = list()

        #call number
        self.callnum = 0

        #Do we really need this F*cking global flag
        self.incall = False
        self.curcall = None

    def findPid(self):
        '''
        description: process may restart, so pid is a list
        :return:
        '''
        for index, line in enumerate(self.loglines):
            fields = line.split()
            fruit = self.logutils.findfields(fields)
            pid = fruit['pid']
            #start to find pid
            for index, process in enumerate(ProcessList):
                key = process.getkey()
                name = process.getname()
                plist = process.getpidlist()
                if pid not in self.pids and self.logutils.patterninline(key, line):
                    self.logger.logger.info('found id ' + str(pid) + ' for ' + name)
                    self.pids.append(pid)
                    plist.append(pid)


    def parse(self):
        '''
        1. pass pid lines
        2. pattern match
        3. pattern handler
        4. draw the graph, csv,
        :return:
        '''
        #find all pids
        self.findPid()

        #handle each patten by pid
        for index, line in enumerate(self.loglines):
            fields = line.split()
            fruit = self.logutils.findfields(fields)
            pid = fruit['pid']
            for index, process in enumerate(ProcessList):
                plist = process.getpidlist()
                pevent = process.getpevent()
                if pid in plist:
                    #then we handle the event
                    elist = pevent.geteventlist()
                    for eindex, event in enumerate(elist):
                        key = event['key']
                        groupnum = event['groupnum']
                        color = event['color']
                        eventHandler = event['eventHandler']

                        regex = re.compile(key)
                        result = regex.search(line)
                        if result:
                            #redirect output
                            with open(self.trimlog, 'a+') as trimlog:
                                trimlog.write(line)

                            #start to handle event, pass the mflow instance
                            handlerobj = eventHandler(result, color, groupnum, mflow=self, fruit=fruit)
                            eventdict = handlerobj.getret()

    def dumpcalllist(self):
        self.logger.logger.info('Totally Call number is ' + str(self.callnum))
        for cindex, call in enumerate(self.calllist):
            call.dumpcall()

    def exportexcel(self):
        # generate sheet named by VT_Call_number_sendstat/recvstat
        wb = excel()
        firstws = wb.workbook.active
        # the first sheet is always sendstat of call 1

        for cindex, call in enumerate(self.calllist):
            #one call will have two sheets: send, recv
            if cindex == 0:
                # the first sheet is always created.
                firstws.title = "VTCall_1_sendstat"

                header = ['time', 'input fps', 'encode fps', 'encode bitrate']
                firstws.append(header)
                for sindex in range(0, call.sendstat['num']):
                    onerow = list()
                    # excel need digits instead of chars
                    onerow.append(call.sendstat['timestamp'][sindex])
                    onerow.append(int(call.sendstat['inputfps'][sindex]))
                    onerow.append(int(call.sendstat['encodefps'][sindex]))
                    onerow.append(int(call.sendstat['encodebps'][sindex])/1000)
                    firstws.append(onerow)
                # set axis
                linechartone = LineChart()
                linechartone.title = "Send Statistics"
                linechartone.y_axis.title = "fps"
                linechartone.x_axis.title = "timestamp"
                linechartone.witdh = 20
                linechartone.height = 10
                #self.logger.logger.info('height is ' + str(linechart.height) + ', width is ' + str(linechart.width))
                #linechart.y_axis.scaling.min = 0
                #linechart.y_axis.scaling.max = 100
                data = Reference(firstws, min_col=2, min_row=1, max_col=3, max_row=call.sendstat['num']+1)
                linechartone.add_data(data, titles_from_data=True)
                dates = Reference(firstws, min_col=1, min_row=2, max_row=call.sendstat['num']+1)
                linechartone.set_categories(dates)



                linecharttwo = LineChart()
                linecharttwo.y_axis.title = "encode kbps"
                linecharttwo.y_axis.axId = 200
                # Display y-axis of the second chart on the right by setting it to cross the x-axis at its maximum
                linechartone.y_axis.crosses = "max"

                # data
                bardata = Reference(firstws, min_col=4, min_row=1, max_row=call.sendstat['num']+1)
                linecharttwo.add_data(bardata, titles_from_data=True)
                linecharttwo.set_categories(dates)

                linechartone += linecharttwo
                chartcell = 'A' + str(call.sendstat['num'] + 3)
                firstws.add_chart(linechartone, chartcell)


                secondws = wb.workbook.create_sheet(title="VTCall_1_recvstat")
                newheader = ['time stamp', 'recvfps', 'recvbps', 'jitter', 'rtt', 'loss']
                secondws.append(newheader)
                rownum = min(call.recvstat['num'], call.recvstat['rtt'])
                for rindex in range(0, rownum):
                    onerow = list()
                    # excel need digits instead of chars
                    onerow.append(call.recvstat['timestamp'][rindex])
                    onerow.append(int(call.recvstat['recvfps'][rindex]))
                    onerow.append(int(call.recvstat['recvbps'][rindex])/1000)
                    onerow.append(int(call.recvstat['jitter'][rindex]))
                    onerow.append(int(call.recvstat['rtt'][rindex]))
                    onerow.append(int(call.recvstat['loss'][rindex]))
                    secondws.append(onerow)

                #fps, bps
                linechartone = LineChart()
                linechartone.title = "Recv Statistics"
                linechartone.y_axis.title = "recv fps"
                linechartone.x_axis.title = "timestamp"
                linechartone.witdh = 20
                linechartone.height = 10
                data = Reference(secondws, min_col=2, min_row=1, max_col=2, max_row=rownum+1)
                linechartone.add_data(data, titles_from_data=True)
                linechartone.set_categories(dates)

                linecharttwo = LineChart()
                linecharttwo.y_axis.title = "recv kbps"
                linecharttwo.y_axis.axId = 200
                # Display y-axis of the second chart on the right by setting it to cross the x-axis at its maximum
                linechartone.y_axis.crosses = "max"

                # data
                bardata = Reference(secondws, min_col=3, min_row=1, max_row=rownum+1)
                linecharttwo.add_data(bardata, titles_from_data=True)
                linecharttwo.set_categories(dates)

                linechartone += linecharttwo
                chartcell = 'I1'
                secondws.add_chart(linechartone, chartcell)


                #jitter, rtt
                linechartone = LineChart()
                linechartone.title = "Recv Qos"
                linechartone.y_axis.title = "jitter"
                linechartone.x_axis.title = "timestamp"
                linechartone.witdh = 20
                linechartone.height = 10
                data = Reference(secondws, min_col=4, min_row=1, max_col=4, max_row=rownum+1)
                linechartone.add_data(data, titles_from_data=True)
                linechartone.set_categories(dates)

                linecharttwo = LineChart()
                linecharttwo.y_axis.title = "rtt"
                linecharttwo.y_axis.axId = 200
                # Display y-axis of the second chart on the right by setting it to cross the x-axis at its maximum
                linechartone.y_axis.crosses = "max"

                # data
                bardata = Reference(secondws, min_col=5, min_row=1, max_row=rownum+1)
                linecharttwo.add_data(bardata, titles_from_data=True)
                linecharttwo.set_categories(dates)

                linechartone += linecharttwo
                chartcell = 'I30'
                secondws.add_chart(linechartone, chartcell)



                #loss
                linechartone = LineChart()
                linechartone.title = "Recv Loss"
                linechartone.y_axis.title = "loss"
                linechartone.x_axis.title = "timestamp"
                linechartone.witdh = 20
                linechartone.height = 10
                data = Reference(secondws, min_col=6, min_row=1, max_col=6, max_row=rownum+1)
                linechartone.add_data(data, titles_from_data=True)
                linechartone.set_categories(dates)
                chartcell = 'I60'
                secondws.add_chart(linechartone, chartcell)


            else:
                pass


        wb.workbook.save(self.excel)

if __name__ == '__main__':
    mflow = mflow(logname="./samplelog/main.log")
    mflow.parse()
    mflow.dumpcalllist()
    mflow.exportexcel()
    pass
