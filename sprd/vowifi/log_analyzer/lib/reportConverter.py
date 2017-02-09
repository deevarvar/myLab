# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com
# analyzed result may be changed due to different ui result
# in the main.pdf or in the report

#TODO:
#      1. epdg stop/failed analysis, add detailed cause
#   html
#       1. add html ref link
#       2. go to top
#       3. error table list, td with color

from reportEvent import *



class langBuilder():
    def __init__(self, zh='', en=''):
        self.phrase = dict()
        self.phrase['lang'] = dict()
        self.phrase['lang']['zh'] = zh
        self.phrase['lang']['en'] = en

    def geten(self):
        return self.phrase['lang']['en']

    def getzh(self):
        return self.phrase['lang']['zh']

    def getenzh(self):
        #use <br> to combine
        return self.phrase['lang']['zh'] + "<br>" + self.phrase['lang']['en']

def map2phrase(key, phrasemap):
    if type(phrasemap) is not dict:
        return key
    if key in phrasemap:
        return phrasemap[key].geten()
    else:
        return key

def mapzhphrase(key, phrasemap):
    if type(phrasemap) is not dict:
        return key
    if key in phrasemap:
        return phrasemap[key].getenzh()
    else:
        return key

#S2B phrase
Reports2bphrase = dict()
Reports2bphrase['successed'] = dict()
Reports2bphrase['successed'] = langBuilder(zh="ePDG驻网成功", en="ePDG attach successfully")

Reports2bphrase['failed'] = dict()
Reports2bphrase['failed'] = langBuilder(zh="ePDG驻网失败", en="ePDG attach failed")

Reports2bphrase['stopped'] = dict()
Reports2bphrase['stopped'] = langBuilder(zh="ePDG驻网正常停止", en="ePDG attach stopped")

Reports2bphrase['stopped_abnormally'] = dict()
Reports2bphrase['stopped_abnormally'] = langBuilder(zh="ePDG驻网异常停止", en="ePDG attach stopped abnormally")

#Register callback
Reportregphrase = dict()
Reportregphrase['login_ok'] = dict()
Reportregphrase['login_ok'] = langBuilder(zh="VoWiFi注册成功", en="VoWiFi Registered")

Reportregphrase['login_failed'] = dict()
Reportregphrase['login_failed'] = langBuilder(zh="VoWiFi注册失败", en="VoWiFi Failed to Register")

Reportregphrase['logouted'] = dict()
Reportregphrase['logouted'] = langBuilder(zh="VoWiFi去注册", en="VoWiFi UnRegistered")

Reportregphrase['refresh_ok'] = dict()
Reportregphrase['refresh_ok'] = langBuilder(zh="VoWiFi 刷新注册成功", en="VoWiFi Re-Registered")

Reportregphrase['refresh_failed'] = dict()
Reportregphrase['refresh_failed'] = langBuilder(zh="VoWiFi 刷新注册失败", en="VoWiFi Failed to Re-Registered")

Reportregphrase['state_update'] = dict()
Reportregphrase['state_update'] = langBuilder(zh="VoWiFi注册状态更新", en="VoWiFi RegState Update")


#helper function to construct report
#report definition is in eventdict in eventhandler
#add error event
def constructRegReport(report, eventname, level, errorstr=''):
    report['type'] = ReportType.PHONEEVENT_BASE
    report['event'] = mapzhphrase(eventname, Reportregphrase)
    report['level'] = level
    report['errorstr'] = errorstr
    #add logic to

def constructS2bReport(report, eventname, level, errorstr=''):
    report['type'] = ReportType.PHONEEVENT_BASE
    report['event'] = mapzhphrase(eventname, Reports2bphrase)
    report['level'] = level
    report['errorstr'] = errorstr