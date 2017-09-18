#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

from config import config
from helper.avcevent import *
from helper.mediaevent import *

MEDIANAME="Media"
AVCNAME="SPRDAVC"

class Process():
    def __init__(self, name='', key='', pidlist=None, pevent=None):
        self.name = name
        self.key = key
        if type(pidlist) is list:
            self.pidlist = pidlist
        else:
            self.pidlist = list()

        self.event = pevent

    def getname(self):
        return self.name

    def getpidlist(self):
        return self.pidlist

    def getkey(self):
        return self.key

    def getpevent(self):
        return self.event

    def setpidlist(self, plist):
        if type(plist) is list:
            self.pidlist = plist

    def seteventlist(self, elist):
        if type(elist) is list:
            self.eventlist = elist

globalconfig = config()
mediaprocess = Process(name=MEDIANAME, key=globalconfig.getmkey(), pevent=mediaevent)
avcprocess = Process(name=AVCNAME, key=globalconfig.getavckey(), pevent=avcevent)

ProcessList = list()
ProcessList.append(mediaprocess)
ProcessList.append(avcprocess)

def find_process_by_id(id):
    for index, process in enumerate(ProcessList):
        if id in process.getpidlist():
            return process
        else:
            return None


