# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com

# define struct about vt call statistics
#
from lib.logConf import *


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
            self.logger.logger.info(self.sendstat['timestamp'][sindex] + ', '+self.sendstat['inputfps'][sindex] + ', ' + self.sendstat['encodefps'][sindex]  + ', ' + self.sendstat['encodebps'][sindex])

        self.logger.logger.info('time, recvfps, recvbitrate, jitter, rtt, loss')
        # in case rtt may be out of index, use less one
        for rindex in range(0, min(self.recvstat['num'], self.recvstat['rtt'])):
            self.logger.logger.info(self.recvstat['timestamp'][rindex] + ', '+self.recvstat['recvfps'][rindex] + ', ' + self.recvstat['recvbps'][rindex] + ', '
                                     + self.recvstat['jitter'][rindex] + ', ' + self.recvstat['rtt'][rindex] + ', '+ self.recvstat['loss'][rindex])


    def exportrecvdata(self,output='recv.xlsx'):
        #try rtt first
        pass

    def exportsenddata(self, output='send.xlsx'):
        pass