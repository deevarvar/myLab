#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

#define event structure
from eventhandler import *

class EventType():
    SEPERATOR = 1 #seperator line
    SELFREF = 2   #self reference edge
    EDGE = 3      # normal edge

class Event():
    def __init__(self):
        self.array = list()
        self.name = ''

    def addevent(self, key, module, eventType = EventType.SEPERATOR, eventHandler = MatchOne, color= "black", groupnum=0, display=True):
        oneevent = dict()
        oneevent['key'] =  key
        oneevent['module'] = module
        oneevent['eventType'] = eventType
        oneevent['eventHandler'] = eventHandler
        oneevent['color'] = color
        oneevent['groupnum'] = groupnum
        oneevent['display'] = display
        self.array.append(oneevent)

    def geteventlist(self):
        return self.array