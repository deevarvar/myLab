#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
import sys
import glob


'''
two ways to track logs:
1. by pid, but process may stop, so pid changes
2. by log tags,  but tags can be trivial.

'''

class log_parser():

    pspattern='./process.txt'
    logpattern='./0-main-*log'
    def getpid(self):
        pass
    def getflow(self):
        pass

    for file in glob.glob('./0-main-*log'):
        with open(file) as logfile:
            for line in logfile:
                print line,


if __name__ == '__main__':
    print 'hello'
    lp = log_parser()