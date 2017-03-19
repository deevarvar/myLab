#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
from easygui import *
import os
#egdemo()
import sys
from configobj import ConfigObj,ConfigObjError
import logging
from flowParser import flowParser
from radioParser import radioParser
from samsungParser import samsungParser
from parseImsbr import *
from threading import Thread,Event
import multiprocessing
from lib.newthread import ThreadWithExc, StoppableThread
#sys.path.append('./lib')
import shutil


from lib.logConf import logConf
from lib.utils import utils
from time import gmtime, strftime

path = os.path.dirname(os.path.realpath(__file__))

#TODO:
#   packaging
#   1. add package scripts
#   ui
#   1. add silent mode
#   todo tag: add error exception
#   flowparser
#   1. add ike parsing
#   2. add service, adapter, imscm logic
#   2.1 start from imscm
#   3. error msg indication:
#   4.1 parse ,cause, cause's mo mt is fixed.
#   4.2 b2bua recodereason
#  todo tag/done: 4.3. update analysis
#  todo tag: 4.4  precondition
#  todo tag/done: 4.5 add UE tag, User agent, ue identify
#  todo tag/done:  4.10 refactor samsung's code
#  todo: tag/done:     4.11 add supported/require, expires identification
#  todo tag/not_to_do: 4.6 split png by call-id
#  todo tag/done: 4.7 add wifi calling msg, airplane mode, wifi calling, wifi connect
#  todo tag/postpone: 4.9 msg init, there should be class to init the msg
#  todo tag/done: 4.12 add sdp parsing: a=rtpmap , a=fmtp
#  todo tag:   4.13 adapter call id record, flow display
#  fixme tag: if file name is too long, open file may fail

#  todo tag: 5.1 handover
#  todo tag/done:  5.1.1 add p-access-network-type, P-associate-uri
#       todo:   tag:  5.1.2 procedure overview
#       todo:   tag/done:  5.1.3 ho's vowifi at command
#       todo:   tag/low prio:   at command like atd, etc(too much, just add some)
#       todo:   tag/done:  trim at log
#       todo:   tag/done: add main/radio/kernel interface to record all log pairs,
#       todo:   tag/done: 5.1.4 merge radio/main logs
#       todo:

#       todo:   tag/done: 5.1.5 add imsbr
#       todo:   tag/done: 5.1.6 add optimization about log tool: search event should only be called , when pid is correct.
#       todo:   tag/done: add security ping printing
#           SecurityS2bBinder: INFO: ping www.bing.com result true
#           ImsCM NetworkUtils: Local IP address is: 2405:204:1a86:7601::1150:a8b0, P-CSCF IP address is: 2405:200:330:1581::21, Ping IP address is reachable
#       todo:   tag/low prio: add ims flow
#       todo:   4.16 tag: overview flow
#       todo:   4.17 tag/done: find the log correctly
#       todo:   tag:  Get the login failed retry callback with code add log
#web page tag:
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
            self.utils = utils(configpath='./')

            self.atmsgs = ''

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % ('config.ini', e)



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
        title = 'VoWifi log tool version: ' + str(self.version)
        buttonboxmsg = 'Please open a directory which contains slog.'
        ylogstring = 'Open the ylog dir'
        samsungfile = "Open Samsung log file"

        choices = [ylogstring, samsungfile , 'Exit']
        choice = buttonbox(buttonboxmsg, title = title, choices = choices)
        if choice != 'Exit':

            if choice == ylogstring:

                takestime = 'NA'
                realmainlog = None

                folder = diropenbox()

                if not folder:
                    msgbox('please relaunch and open a directory.')
                    exit()
                else:
                    helper = utils(configpath='./')
                    self.logger.logger.info('folder is ' + folder)
                    matches = helper.findlogs(folder)

                    '''
                    print matches
                    import time
                    time.sleep(50)
                    '''
                    for index, filedict in enumerate(matches):
                        #call the real parser

                        self.curtimestamp = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
                        mainlog = filedict['mainlog']
                        radiolog = filedict['radiolog']
                        kernellog = filedict['kernellog']

                        #actually mainlog will always exist

                        #first of all , get radio log , if exist
                        if not mainlog:
                            continue
                        self.logger.logger.info('mainlog is ' + mainlog);
                        mainlogrealpath = os.path.realpath(mainlog)
                        shortname = os.path.basename(mainlogrealpath)
                        dirname = os.path.dirname(mainlogrealpath)
                        outputdir = dirname + '/' + shortname.split('.')[0]


                        self.utils.mkdirp(outputdir)

                        if kernellog:
                            print 'kernel log is ' + kernellog
                            krealpath = os.path.realpath(kernellog)
                            kshortname = os.path.basename(kernellog)
                            kernel_results = parse_imsbr(krealpath)
                            #FIXME: output imsbr log to diagrams
                            kernel_outputdir = outputdir + '/diagrams/'
                            self.utils.mkdirp(kernel_outputdir)
                            imsbrlog = kernel_outputdir + '/'+ kshortname.split('.')[0] +'-imsbr.log'
                            with open(imsbrlog, 'w') as imsbrlog:
                                for dict in kernel_results:
                                    imsbrlog.write("line%d: %s %s \n" %(dict["lineno"], dict["timestamp"], dict["msg"]))

                        if radiolog:
                            rp = radioParser(logname = radiolog, outputdir = outputdir)
                            self.atmsgs = rp.getflow()
                            rp.assembleStr()
                            rp.drawAllDiag()

                        realmainlog =  mainlog
                        fp = flowParser(logname = mainlog, atmsgs=self.atmsgs)
                        len = fp.getFlow()
                        self.msglen =  len
                        self.logger.logger.info('sip msgs len is ' + str(len))

                        #self.popupmsg(file)
                        #msgbox(msg)
                        #t = ThreadWithExc(target=self.popupthread,args=(currentfile,))
                        #t.start()
                        fp.parseFlow()
                        takestime = fp.drawAllDiag()
                        if takestime == -1:
                            self.logger.logger.info('exit the parser unexpectedly!')
                            exit(-1)
                        #fp.drawLemonDiag()

                        #t.raiseExc(SystemExit)


                popupstr = ''
                filestr = ''
                if realmainlog:
                    fsize = os.path.getsize(realmainlog)
                    name = os.path.basename(realmainlog)
                    filestr = "file is " + name + '\n' + "file size is " + str(self.utils.humansize(fsize)) + '\n'
                popupstr = "Finishing parsing\n"
                popupstr += filestr
                popupstr += "It takes "+ takestime + " seconds"
                self.logger.logger.info(popupstr)
                msgbox(popupstr)


            elif choice == samsungfile:
                file = fileopenbox()
                if not file:
                    msgbox('please relaunch and open a valid samsung log.')
                    exit()
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









