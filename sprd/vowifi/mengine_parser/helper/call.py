# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com

# define struct about vt call statistics
#
from lib.logConf import *
from helper.excelhelper import *


class Call:
    def __init__(self):
        self.time = dict()
        self.time['start'] = ''  # incoming/outgoing
        self.time['end'] = ''   # callend
        self.streamid = ''
        self.logger = logConf()


class AudioCall(Call):
    def __init__(self):
        Call.__init__(self)
        # TODO: add audio stat later
        pass

    def dumpcall(self):
        pass


class VtCall(Call):
    def __init__(self):
        # if call __init__. should call __init__
        Call.__init__(self)

        # video first sps, pps, key frame
        self.time['firstsps'] = ''
        self.time['firstpps'] = ''
        self.time['kframe'] = ''

        # camera info
        self.camerainfo = dict()
        self.camerainfo['camid'] = ''
        self.camerainfo['minfps'] = ''
        self.camerainfo['maxfps'] = ''
        self.camerainfo['width'] = ''
        self.camerainfo['height'] = ''

        # codec info
        self.codec = dict()
        self.codec['payload'] = ''
        self.codec['name'] = ''
        self.codec['cvo'] = False
        self.codec['videoas'] = ''

        # use openpyxl to draw excel
        # openpyxl need list of list like [ [1,2,3], [4, 5, 6]]
        # send statistics
        self.sendstat = dict()
        self.sendstat['num'] = 0
        self.sendstat['timestamp'] = list()
        # inputfps, encodefps, encodebps
        self.sendstat['inputfps'] = list()
        self.sendstat['encodefps'] = list()
        self.sendstat['encodebps'] = list()

        # recv statistics
        self.recvstat = dict()
        self.recvstat['timestamp'] = list()
        # maxseq is used to indicate if packet num is changed.
        self.recvstat['maxseq'] = 0
        self.recvstat['num'] = 0
        # recvfps, recvbps, jitter, rtt, loss
        self.recvstat['recvfps'] = list()
        self.recvstat['recvbps'] = list()
        self.recvstat['jitter'] = list()
        self.recvstat['rtt'] = list()
        self.recvstat['loss'] = list()

        # some column index variable in excel
        self.index = dict()
        self.index['timestamp'] =1
        self.index['inputfps'] = 2
        self.index['encodefps'] = 3
        self.index['encodebps'] = 4
        self.index['recvfps'] = 2
        self.index['recvbps'] = 3
        self.index['jitter'] = 4
        self.index['rtt'] = 5
        self.index['loss'] = 6

        # some width/height in excel, used to place the chart..
        # will use get_column_letter to change to column letter
        # 1->A, 27->A1, 26->Z
        self.sendwidth = 4
        self.recvwidth = 6

        # height need to updated with rows...
        self.sendheight = 0
        self.recvheight = 0

    def assemblerecvpkt(self, recvfps, recvbitrate):
        self.recvstat['num'] += 1
        onepacket = list()
        onepacket.append(recvfps)
        onepacket.append(recvbitrate)
        self.recvstat['pktlist'].append(onepacket)

    def dumpcall(self):
        """
        TODO: better output and format
        :return:
        """
        self.logger.logger.info('call start is ' + self.time['start'])
        self.logger.logger.info('call start is ' + self.time['end'])
        self.logger.logger.info('cam resolution is ' + self.camerainfo['width'] + 'x' + self.camerainfo['height'])
        self.logger.logger.info('codec payload is ' + self.codec['payload'] + ', name is ' + self.codec['name'] +
                                ', cvo is ' + str(self.codec['cvo']) + ', videoas is ' + self.codec['videoas'])
        self.logger.logger.info('send pkt num is '+ str(self.sendstat['num']) +', recv pkt num is ' + str(self.recvstat['num']))

        self.logger.logger.info('time, input fps, encode fps, encode bitrate')
        for sindex in range(0, self.sendstat['num']):
            self.logger.logger.info('sindex is ' + str(sindex)+ ','+ self.sendstat['timestamp'][sindex] + ', '+self.sendstat['inputfps'][sindex] + ', ' + self.sendstat['encodefps'][sindex]  + ', ' + self.sendstat['encodebps'][sindex])

        self.logger.logger.info('time, recvfps, recvbitrate, jitter, rtt, loss')
        # in case rtt may be out of index, use less one
        self.logger.logger.info('fps num is ' + str(self.recvstat['num']) + ', rtt num is ' + str(len(self.recvstat['rtt'])))
        for rindex in range(0, min(self.recvstat['num'], len(self.recvstat['rtt']))):
            self.logger.logger.info('rindex is '+ str(rindex) + ','+ self.recvstat['timestamp'][rindex] + ', '+self.recvstat['recvfps'][rindex] + ', ' + self.recvstat['recvbps'][rindex] + ', '
                                     + self.recvstat['jitter'][rindex] + ', ' + self.recvstat['rtt'][rindex] + ', '+ self.recvstat['loss'][rindex])

    def sendsheettitle(self, num):
        return "VTCall_" + str(num) +"_sendstat"

    def recvsheettitle(self, num):
        return "VTCall_" + str(num) +"_recvstat"

    def sendheader(self):
        header = ['time', 'input fps', 'encode fps', 'encode bitrate']
        return header

    def recvheader(self):
        header = ['time stamp', 'recvfps', 'recvbps', 'jitter', 'rtt', 'loss']
        return header

    # if possbile may add extra data output file
    def gensendsheet(self, sendsheet):

        header = self.sendheader()
        sendsheet.append(header)
        rownum = self.sendstat['num']
        for sindex in range(0, rownum):
            onerow = list()
            onerow.append(self.sendstat['timestamp'][sindex])
            # excel need digits instead of chars
            onerow.append(int(self.sendstat['inputfps'][sindex]))
            onerow.append(int(self.sendstat['encodefps'][sindex]))
            onerow.append(int(self.sendstat['encodebps'][sindex])/1000)
            sendsheet.append(onerow)
            self.sendheight += 1
        self.sendheight += 1

        if rownum >= 1:
            fpschart = ChartInfo(title="Send Statistics", xtitle="timestamp", ytitle="fps")
            fpsref = ReferenceInfo(min_col=self.index['inputfps'], min_row=1, max_col=self.index['encodefps'], max_row=rownum+1)
            encodechart = ChartInfo(title="Send Statistics", xtitle="timestamp", ytitle="encode kbps")
            encoderef = ReferenceInfo(min_col=self.index['encodebps'], min_row=1, max_col=self.index['encodebps'],  max_row=rownum+1)
            # not hardcoded here,  it is G3
            chartcell = getcolumnletter(self.sendwidth + WIDTH_SPACE) + str(HEIGHT_START)

            addtwoaxischart(sendsheet, fpschart, fpsref, encodechart, encoderef, chartcell)

    def genrecvsheet(self, recvsheet):
        # fps && bps with two axis
        newheader = self.recvheader()
        recvsheet.append(newheader)
        rownum = min(self.recvstat['num'], len(self.recvstat['rtt']))
        for rindex in range(0, rownum):
            onerow = list()
            # excel need digits instead of chars
            onerow.append(self.recvstat['timestamp'][rindex])
            onerow.append(int(self.recvstat['recvfps'][rindex]))
            onerow.append(int(self.recvstat['recvbps'][rindex])/1000)
            onerow.append(int(self.recvstat['jitter'][rindex]))
            onerow.append(int(self.recvstat['rtt'][rindex]))
            onerow.append(int(self.recvstat['loss'][rindex]))
            recvsheet.append(onerow)
            self.recvheight += 1
        self.recvheight += 1

        if rownum >=1:
            recvfpschart = ChartInfo(title="Recv Statistics", xtitle="timestamp", ytitle="recv fps")
            recvref = ReferenceInfo(min_col=self.index['recvfps'], min_row=1, max_col=self.index['recvfps'], max_row=rownum+1)
            recvbpschart = ChartInfo(title="Recv Statistics", xtitle="timestamp", ytitle="recv kbps")
            recvbpsref = ReferenceInfo(min_col=self.index['recvbps'], min_row=1, max_col=self.index['recvbps'], max_row=rownum+1)

            # we will draw three chart here
            chartcell = getcolumnletter(self.recvwidth + WIDTH_SPACE) + str(HEIGHT_START + HEIGHT_SPACE)
            addtwoaxischart(recvsheet, recvfpschart, recvref, recvbpschart, recvbpsref, chartcell)

            # jitter && rtt with two axis
            jitterchart = ChartInfo(title="Recv Qos", xtitle="timestamp", ytitle="jitter")
            jitterref = ReferenceInfo(min_col=self.index['jitter'], min_row=1, max_col=self.index['jitter'], max_row=rownum+1)
            rttchart = ChartInfo(title="Recv Qos", xtitle="timestamp", ytitle="rtt")
            rttref = ReferenceInfo(min_col=self.index['rtt'], min_row=1, max_col=self.index['rtt'], max_row=rownum+1)
            chartcell = getcolumnletter(self.recvwidth + WIDTH_SPACE) + str(2*HEIGHT_START)
            addtwoaxischart(recvsheet, jitterchart, jitterref, rttchart, rttref, chartcell)

            # loss
            chartinfo = ChartInfo(title="Recv Loss", xtitle="timestamp", ytitle="loss")
            referenceinfo = ReferenceInfo(min_col=self.index['loss'] , min_row=1, max_col=self.index['loss'] , max_row=rownum+1)
            chartcell = getcolumnletter(self.recvwidth + WIDTH_SPACE) + str(HEIGHT_START + 2*HEIGHT_SPACE)
            addoneaxischart(recvsheet, chartinfo, referenceinfo, chartcell)
