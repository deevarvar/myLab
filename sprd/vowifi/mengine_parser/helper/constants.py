#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

class Msglevel():
    DEBUG = 1
    INFO = 2
    NORMAL = 3
    WARNING = 4
    ERROR = 5


def maplevel2color(level):
    if level == Msglevel.INFO:
        return "blue"
    elif level == Msglevel.WARNING:
        return "brown"
    elif level == Msglevel.ERROR:
        return "red"
    elif level == Msglevel.NORMAL:
        return "green"
    else:
        return "black"