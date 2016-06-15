#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
from easygui import *
#egdemo()
import sys
from flowParser import flowParser
sys.path.append('./lib')
from logConf import logConf
from utils import utils





class loggergui():
    def __init__(self):
        self.logger = logConf()

    def run(self):
        # util will do the search
        # util will create result dir
        # flowParser only parse one file

        folder = diropenbox()

        if not folder:
            msgbox('please relaunch and open a directory.')
            exit
        else:
            helper = utils(configpath='./')
            matches = helper.findlogs(folder)
            for index,file in enumerate(matches):
                print file

        #file = fileopenbox()
if __name__ == '__main__':
    gui = loggergui()
    gui.run()









