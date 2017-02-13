# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com
# analyzed result may be changed due to different ui result
# in the main.pdf or in the report

#Done:
#      1. done: epdg stop/failed analysis, add detailed cause
#      2. done: error table list, td with color
#      3. add html ref link,
#      4. link on the error text
#      5. error details display
#      5.1 rewrite updatereportEvent and constructreportEvent, add field

#TODO:
#       6. add catagory to display, top occurence and timestamp (Definition of Done: DoD )
#       6.1 user action,  phone, scenario
#       7. add ho, call, user action
#       8. add normal scenarioes details
#       8.1 timestamps, etc
#       10. process duration: s2b, reg, ho, call
#       11. go to top
#

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
        return self.phrase['lang']['en'] + "<br>" + self.phrase['lang']['zh']

class reportBuilder():
    def __init__(self, type, event, level, errorstr=''):
        self.report = dict()
        self.report['type'] = type
        self.report['event'] = event
        self.report['level'] = level
        self.report['errorstr'] = errorstr

    def getreport(self):
        return self.report


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

#Handover actions
ReportHandoverphrase = dict()
ReportHandoverphrase['wificonn'] = dict()
ReportHandoverphrase['wificonn'] = langBuilder(zh="连上WiFi", en="WiFi is Connected")

ReportHandoverphrase['wifidisconn'] = dict()
ReportHandoverphrase['wifidisconn'] = langBuilder(zh="WiFi断开连接", en="WiFi is Disconnected")


ReportHandoverphrase['airon'] = dict()
ReportHandoverphrase['airon'] = langBuilder(zh="打开飞行模式", en="open airplane mode")


ReportHandoverphrase['airoff'] = dict()
ReportHandoverphrase['airoff'] = langBuilder(zh="关闭飞行模式", en="close airplane mode")

ReportHandoverphrase['enwfc'] = dict()
ReportHandoverphrase['enwfc'] = langBuilder(zh="打开WiFi-Calling", en="Enable WiFi-Calling")

ReportHandoverphrase['disenwfc'] = dict()
ReportHandoverphrase['disenwfc'] = langBuilder(zh="关闭WiFi-Calling", en="Disable WiFi-Calling")

ReportHandoverphrase['idlehowifi'] = dict()
ReportHandoverphrase['idlehowifi'] = langBuilder(zh="Idle切换到VoWiFi", en="Idle Handover to VoWiFi")
ReportHandoverphrase['idleholte'] = dict()
ReportHandoverphrase['idleholte'] = langBuilder(zh="Idle切换到VoLTE", en="Idle Handover to VoLTE")
ReportHandoverphrase['callhowifi'] = dict()
ReportHandoverphrase['callhowifi'] = langBuilder(zh="电话中切到VoWiFi", en="Handover to VoWiFi in Call")
ReportHandoverphrase['callholte'] = dict()
ReportHandoverphrase['callholte'] = langBuilder(zh="电话中切到VoLTE", en="Handover to VoLTE in Call")

#write a report builder

#helper function to construct report
#report definition is in eventdict in eventhandler
#add error event
def constructReport(type=ReportType.PHONEEVENT_BASE, event='', level=Msglevel.WARNING, errorstr=''):
    event = event
    level = level
    errorstr = errorstr
    builder = reportBuilder(type=type, event=event, level=level, errorstr=errorstr)
    return builder.getreport()


