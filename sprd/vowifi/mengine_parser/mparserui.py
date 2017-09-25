# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com


from lib.logConf import logConf
from easygui import *
from mflow_parser import *
from config import *
from datetime import *



logger = logConf()
config = config()
title = 'media engine log parser version: ' + str(config.getversion())
buttonboxmsg = 'Please select a main log:'
ylogstring = 'Open a main log'
choices = [ylogstring,  'Exit']
choice = buttonbox(buttonboxmsg, title = title, choices = choices)
if choice != 'Exit':
    if choice == ylogstring:
        mainlog = fileopenbox()
        if not mainlog:
            msgbox('please relaunch and open a correct log.')
            exit()
        else:
            mflow = mflow(logname=mainlog)
            starttime = datetime.now()
            mflow.parse()
            mflow.exportexcel()
            endtime = datetime.now()
            duration = endtime - starttime
            popupstr = "Finishing parsing\n"
            popupstr += mainlog
            popupstr += "\nIt takes "+ str(duration) + " seconds"
            logger.logger.info(popupstr)
            msgbox(popupstr)

else:
    exit()
