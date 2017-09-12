#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
import re

#1. utils to handle android logs like main.log, radio.log, kernel.log
#2. find pid by keyword
#3. line grep

class logutils():
    def __init__(self):
        pass

    def checkint(self, s):
        s = s.strip()
        if s[0] in ('-', '+'):
            return s[1:].isdigit()
        return s.isdigit()

    def wordinline(self, word, line):
        if word in line:
            return True
        else:
            return False

    def patterninline(self, pattern, line):
        regex = re.compile(pattern)
        if regex.search(line):
            return True
        else:
            return False

    def findfields(self, fields):
        '''
        log format is changed in android O
        00D347 08-23 19:57:51.585  1205  1254 D LEMON
        :return:
        '''
        datepattern= "\d\d-\d\d"
        dpattern = re.compile(datepattern)
        first = fields[0]
        match = dpattern.match(first)
        fruit = dict()
        fruit['day'] = ""
        fruit['time'] = ""
        fruit['pid'] = ""
        if match:
            fruit['day'] = fields[0]
            fruit['time'] = fields[1]
            fruit['pid'] = fields[2]
        else:
            fruit['day'] = fields[1]
            fruit['time'] = fields[2]
            fruit['pid'] = fields[3]
        #pid should be integer, or return None
        if not self.checkint(fruit['pid']):
            fruit['pid'] = None
        return fruit



if __name__ == "__main__":
    lutils = logutils()
    line = "02D429 08-31 16:18:20.260  4117  4286 I MME     : 16:18:20.260 MVD: INFO: StrmOpen rtp timeout 5 "
    print lutils.patterninline("MME.*MVD", line)