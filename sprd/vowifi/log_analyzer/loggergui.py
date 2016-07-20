#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
from easygui import *
import os
#egdemo()
import sys
from configobj import ConfigObj,ConfigObjError
import logging
from flowParser import flowParser
from samsungParser import samsungParser
from threading import Thread,Event
import multiprocessing
from lib.newthread import ThreadWithExc, StoppableThread
#sys.path.append('./lib')


from lib.logConf import logConf
from lib.utils import utils
from time import gmtime, strftime

path = os.path.dirname(os.path.realpath(__file__))

#TODO:
#   packaging
#   1. add package scripts
#   ui
#   1. add silent mode
#   flowparser
#   1. add ike parsing
#   2. add service, adapter, imscm logic
#   2.1 start from imscm
#   3. error msg indication:
#   4.1 parse reason,cause, cause's mo mt is fixed.
#   4.2 b2bua recode
#  todo tag: 4.3. update analysis
#  todo tag: 4.4  precondition
#  todo tag: 4.5 add UE tag, User agent, ue identify
#  todo tag: 4.6 split png by call-id
#  todo tag/done: 4.7 add wifi calling msg, airplane mode, wifi calling, wifi connect
#  todo 4.8: split the msg: if msg is larger than some value, only generate pdf or png
   #
#  todo tag: 4.9 msg init, there should be class to init the msg
#   web page
#   1. how to display
#   2. overall results, use actdiag

#   3. possible error msg defined in config.ini
#   logparser:
#   1. add ike keys and esp keys parsing
#   2. type payload parsing; delete, notify

# BUG:
# 1. if the first msg is missing , the momt will be wrong.

class loggergui():
    def __init__(self):
        try:
            configfile = path + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.loglevel =  config['logging']['loglevel']
            self.version =  config['utils']['version']
            self.msglen = 0
            print self.loglevel
            print logging.getLevelName(self.loglevel)
            self.logger = logConf(debuglevel=logging.getLevelName(self.loglevel))

            #one sip msg to render diagram's time
            self.estimatetime = config['utils']['estimate']
            self.threadlist = list()

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)



    def popupmsg(self, file):
        len = self.msglen
        self.logger.logger.info('msg len is ' + str(len))
        msg = 'log file is ' + file + '\n'
        msg += 'totally sip/ike msgs are ' + str(len) + '\n'
        esttime = float(self.estimatetime)*int(len)
        timelog = 'estimate time  is ' + str(esttime) + ' seconds'
        msg = msg + timelog
        msgbox(msg)


    def workerthread(self, fileparser):
        pass

    def run(self):
        # util will do the search
        # util will create result dir
        # flowParser only parse one file
        title = 'VoWifi log tool by zhihuay.ye, version: ' + str(self.version)
        buttonboxmsg = 'Please open a directory which contains slog.'
        slogstring = 'Open the slog dir'
        samsungfile = "Open Samsung log file"

        choices = [slogstring, samsungfile , 'Exit']
        choice = buttonbox(buttonboxmsg, title = title, choices = choices)
        if choice != 'Exit':

            if choice == slogstring:


                folder = diropenbox()

                if not folder:
                    msgbox('please relaunch and open a directory.')
                    exit
                else:
                    helper = utils(configpath='./')
                    matches = helper.findlogs(folder)
                    for index,file in enumerate(matches):
                        #call the real parser

                        self.curtimestamp = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
                        #pop up a msg box
                        #self.popupmsg(file)

                        fp = flowParser(file)
                        len = fp.getFlow()
                        self.msglen =  len
                        self.logger.logger.info('sip msgs len is ' + str(len))

                        #self.popupmsg(file)
                            #msgbox(msg)
                        #t = ThreadWithExc(target=self.popupthread,args=(currentfile,))
                        #t.start()
                        fp.parseFlow()
                        fp.drawAllDiag()
                        #fp.drawLemonDiag()

                        #t.raiseExc(SystemExit)

                msgbox('Finish parsing sprd log file')


            elif choice == samsungfile:
                file = fileopenbox()
                if not file:
                    msgbox('please relaunch and open a valid samsung log.')
                    exit
                else:
                    sp = samsungParser(logname=file)
                    sp.getflow()
                    msgbox('Finish parsing file ' + file)
        else:
            return

        #file = fileopenbox()
if __name__ == '__main__':
    gui = loggergui()
    gui.run()









