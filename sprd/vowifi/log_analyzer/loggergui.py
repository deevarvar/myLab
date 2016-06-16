#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
from easygui import *
import os
#egdemo()
import sys
from configobj import ConfigObj,ConfigObjError
import logging
from flowParser import flowParser
sys.path.append('./lib')
from logConf import logConf
from utils import utils

path = os.path.dirname(os.path.realpath(__file__))




class loggergui():
    def __init__(self):
        try:
            configfile = path + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.logger = logConf()
            self.loglevel =  config['logging']['loglevel']
            self.logger = logConf(debuglevel=logging.getLevelName(self.loglevel))

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)


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
                #call the real parser
                fp = flowParser(file)
                fp.getFlow()
                fp.parseFlow()
                fp.drawLemonDiag()


        #file = fileopenbox()
if __name__ == '__main__':
    gui = loggergui()
    gui.run()









