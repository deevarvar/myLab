# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com

from constants import *
from lib.logConf import *
from helper.call import *
from lib.logutils import *

class EventResult:
    def __init__(self):
        self.msglevel = Msglevel.INFO
        self.color = "black"
        self.msg = None
        # report type, default is none, should be set in eventHandler
        self.report = dict()
        self.report['type'] = None
        self.report['event'] = None
        self.report['level'] = Msglevel.INFO
        self.report['errorstr'] = None
        self.report['lineno'] = None
        self.report['line'] = None
        self.report['timestamp'] = None


class EventHandler:
    def __init__(self, match, color, groupnum, mflow, fruit):
        """

        :param match:
        :param color:
        :param groupnum:
        :param mflow:
        :param fruit: fruit is defined in logutils.py, day, time, pid
        :return:
        """

        self.match = match
        self.color = color
        self.groupnum = groupnum
        self.retmsg = EventResult()
        # set the selected color
        self.retmsg.color = color
        self.logger = logConf()

        # the mflow instance used to communicate with main process
        self.mflow = mflow
        self.fruit = fruit
        self.logutils = logutils()

    def handler(self):
        # need to overwrite the handler.
        return None

    '''
       ######### main process #########
    '''
    def getret(self):
        grouplen = len(self.match.groups())
        if self.match and grouplen >= self.groupnum:
            return self.handler()
        else:
            return None


class MatchOne(EventHandler):
    """
    only match one , return one
    """
    def handler(self):
        self.retmsg.msg = self.match.group(1)
        return self.retmsg


class VideoStart(EventHandler):
    """
        video start flag
    """
    def handler(self):
        # what if callend log is missing.
        self.logger.logger.info("new vt call " + str(self.mflow.callnum) + " started")
        self.mflow.callnum += 1
        self.mflow.incall = True
        newcall = VtCall()
        self.mflow.curcall = newcall
        self.mflow.calllist.append(newcall)
        newcall.time['start'] = self.fruit['day'] + ' ' + self.fruit['time']


class VideoStop(EventHandler):
    """
        video start flag
    """
    def handler(self):
        self.logger.logger.info("vt call "+ str(self.mflow.callnum) +" ended")
        self.mflow.incall = False
        self.mflow.curcall.time['end'] = self.fruit['day'] + ' ' + self.fruit['time']
        start = self.mflow.curcall.time['start']
        end = self.mflow.curcall.time['end']
        self.mflow.curcall.time['duration'] = str(self.logutils.converttime(end) - self.logutils.converttime(start))

class AttachCam(EventHandler):
    def handler(self):
        # four params: stream id, cam id, facing , orientation
        if self.mflow.incall:
            streamid = self.match.group(1).strip()
            camid = self.match.group(2).strip()
            # get current call and check if call exists.
            self.mflow.curcall.streamid = streamid
            self.mflow.curcall.camerainfo['camid'] = camid


class CamFps(EventHandler):
    def handler(self):
        # min fps, max fps
        if self.mflow.incall:
            minfps = self.match.group(1).strip()
            maxfps = self.match.group(2).strip()
            # divide 1000 here
            self.mflow.curcall.camerainfo['minfps'] = str(int(minfps)/1000)
            self.mflow.curcall.camerainfo['maxfps'] = str(int(maxfps)/1000)


class VtResolution(EventHandler):
    def handler(self):
        # width, height
        if self.mflow.incall:
            width = self.match.group(1).strip()
            height = self.match.group(2).strip()
            self.mflow.curcall.camerainfo['width'] = width
            self.mflow.curcall.camerainfo['height'] = height


class SetCodec(EventHandler):
    def handler(self):
        # seven param: streamid, name, payload, bitrate, frame, width, height
        if self.mflow.incall:
            name = self.match.group(2).strip()
            payload = self.match.group(3).strip()
            self.mflow.curcall.codec['name'] = name
            self.mflow.curcall.codec['payload'] = payload


class SetCvo(EventHandler):
    def handler(self):
        if self.mflow.incall:
            cvoid = self.match.group(1).strip()
            self.mflow.curcall.codec['cvo'] = 'Supported'
            self.mflow.curcall.codec['cvoid'] = cvoid

class VideoAs(EventHandler):
    def handler(self):
        if self.mflow.incall:
            videoas = self.match.group(1).strip()
            self.mflow.curcall.codec['videoas'] = videoas


class SendStat(EventHandler):
    def handler(self):
        # three params: input fps, encode fps, encode bitrate
        if self.mflow.incall:
            inputfps = self.match.group(1).strip()
            encodefps =  self.match.group(2).strip()
            encodebps  = self.match.group(3).strip()
            sendstat = self.mflow.curcall.sendstat
            sendstat['num'] += 1
            sendstat['inputfps'].append(inputfps)
            sendstat['encodefps'].append(encodefps)
            sendstat['encodebps'].append(encodebps)
            timestamp = self.fruit['time']
            sendstat['timestamp'].append(timestamp)


class RecvStat(EventHandler):
    def handler(self):
        # four params: recvfps, recvbitrate, loss, jitter, maxseq
        if self.mflow.incall:
            recvfps = self.match.group(1).strip()
            recvbps = self.match.group(2).strip()
            loss =  self.match.group(3).strip()
            jitter = self.match.group(4).strip()
            maxseq = self.match.group(5).strip()
            # NOTE: if maxseq is not changed, we skip this report.
            if str(maxseq) != str(self.mflow.curcall.recvstat['maxseq']):
                recvstat = self.mflow.curcall.recvstat
                recvstat['maxseq'] = maxseq
                recvstat['num'] += 1
                recvstat['recvfps'].append(recvfps)
                recvstat['recvbps'].append(recvbps)
                timestamp = self.fruit['time']
                recvstat['timestamp'].append(timestamp)

            else:
                self.logger.logger.info("maxseq " + maxseq + " not updated so packet is not updated in call " + str(self.mflow.callnum))

class VideoRtt(EventHandler):
    def handler(self):
        # one param: jitter, rtt, loss ratio
        # only caculate it when active call
        #
        if self.mflow.incall and self.mflow.curcall.recvstat['num']:
            jitter = self.match.group(1).strip()
            vrtt = self.match.group(2).strip()
            loss = self.match.group(3).strip()
            # use MVD's rtt, jitter, loss
            recvstat = self.mflow.curcall.recvstat
            recvstat['jitter'].append(jitter)
            recvstat['rtt'].append(vrtt)
            recvstat['loss'].append(loss)


class GetNal(EventHandler):
    def handler(self):
        if self.mflow.incall:
            naltype = self.match.group(1).strip()
            if naltype == '7':
                if not self.mflow.curcall.time['firstsps']:
                   self.mflow.curcall.time['firstsps'] = self.fruit['time']

            elif naltype == '8':
                if not self.mflow.curcall.time['firstpps']:
                   self.mflow.curcall.time['firstpps'] = self.fruit['time']
            else:
                self.logger.logger.info('unknown nal type ' + naltype)
