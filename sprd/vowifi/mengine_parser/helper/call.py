#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

#define struct about vt call statistics
#
from lib.logConf import *

class Call():
    def __init__(self):
        self.time = dict()
        self.time['start'] = '' #incoming/outgoing
        self.time['end'] = ''   #callend
        self.streamid = ''
        self.logger = logConf()

class AudioCall(Call):
    def __init__(self):
        Call.__init__(self)
        #TODO: add audio stat later
        pass

    def dumpCall(self):
        pass


class VtCall(Call):
    def __init__(self):
        #if call __init__. should call __init__
        Call.__init__(self)

        #video first sps, pps, key frame
        self.time['firstsps'] = ''
        self.time['firstpps'] = ''
        self.time['kframe'] = ''

        #camera info
        self.camerainfo = dict()
        self.camerainfo['camid'] = ''
        self.camerainfo['minfps'] = ''
        self.camerainfo['maxfps'] = ''
        self.camerainfo['width'] = ''
        self.camerainfo['height'] = ''

        #codec info
        self.codec = dict()
        self.codec['payload'] = ''
        self.codec['name'] = ''
        self.codec['cvo'] = False
        self.codec['videoas'] = ''

        #send statistics
        self.sendstat = dict()
        self.sendstat['outfps'] = list()
        self.sendstat['encodefps'] = list()
        self.sendstat['bitrate'] = list()

        #recv statistics
        self.recvstat = dict()
        self.recvstat['recvfps'] = list()
        self.recvstat['decodefps'] = list()
        self.recvstat['bitrate'] = list()
        self.recvstat['jitter'] = list()
        self.recvstat['rtt'] = list()


    def dumpcall(self):
        self.logger.logger.info('call start is ' + self.time['start'])
        self.logger.logger.info('call start is ' + self.time['end'])
        self.logger.logger.info('cam resolution is ' + self.camerainfo['width'] + 'x' + self.camerainfo['height'])