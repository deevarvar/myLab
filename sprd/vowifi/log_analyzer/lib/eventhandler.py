#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
#some event helper for searchEvent in flowParser.py


import re

class Msglevel():
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

def maplevel2color(level):
    if level <= Msglevel.INFO:
        return "black";
    elif level == Msglevel.WARNING:
        return "blue"
    else:
        return "red"

class eventdict():
    def __init__(self):
        self.msglevel = Msglevel.INFO
        self.color = "black"
        self.msg = None


def matchone(match):
    '''
    return the first match one
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    retmsg = eventdict()
    if match and grouplen >= 1:
        retmsg.msg = match.group(1)
        return retmsg
    else:
        return None

def geticon(match):
    '''
    get vowifi/volte icon
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    iconstr = None
    level = Msglevel.INFO
    retmsg = eventdict()
    if match and grouplen >=2:
        ltestr = match.group(1)
        wifistr = match.group(2)
        if ltestr == "true":
            if wifistr == "true":
                iconstr = "show VoWiFi and VoLTE signal icons"
                level = Msglevel.ERROR
            else:
                iconstr = "show VoLTE signal icon"
                level = Msglevel.WARNING

        else:
            if wifistr == "true":
                iconstr = "show VoWiFi signal icon"
                level = Msglevel.WARNING
            else:
                iconstr = "No VoLTE/VoWiFi signal icon"
                level = Msglevel.WARNING
        retmsg.msg = iconstr
        retmsg.level = level
        retmsg.color = maplevel2color(level)
        return retmsg
    else:
        return None

def imsregaddr(match):
    '''
    set ims reg addr
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    retmsg = eventdict()
    if match and grouplen >= 1:
        regaddr = match.group(1)
        retmsg.msg = "SetIMSRegAddr:\n" + regaddr
        return retmsg
    else:
        return None

if __name__ == '__main__':
    key = 'abc'
    line = "abc"
    pattern = re.compile(key)
    match = pattern.search(line)
    print matchone(match)