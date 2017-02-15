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
#      11. back to top
#TODO:
#       6. add catagory to display, top occurence and timestamp (Definition of Done: DoD )
#       6.1 user action,  phone, scenario
#       7. add ho, call, user action
#       8. add normal scenarioes details
#       8.1 timestamps, etc
#       10. process duration: s2b, reg, ho, call
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
ReportHandoverphrase['voiceqos2lte'] = dict()
ReportHandoverphrase['voiceqos2lte'] = langBuilder(zh="语音通话质量差切换到Volte", en="Handover to VoLTE Due to Poor Voice Quality")
ReportHandoverphrase['videoqos2lte'] = dict()
ReportHandoverphrase['videoqos2lte'] = langBuilder(zh="视频通话质量差切换到Volte", en="Handover to VoLTE Due to Poor Video Quality")

ReportHandoverphrase['incallrssiho2wifi'] = dict()
ReportHandoverphrase['incallrssiho2wifi'] = langBuilder(zh="通话中WiFi信号好切换到VoWiFi", en="Handover to VoWiFi In Call Due to Strong WiFi Signal")

ReportHandoverphrase['rssiho2wifi'] = dict()
ReportHandoverphrase['rssiho2wifi'] = langBuilder(zh="WiFi信号好切换到VoWiFi", en="Handover to VoWiFi From VoLTE Due to Strong WiFi Signal")

ReportHandoverphrase['autowifi'] = dict()
ReportHandoverphrase['autowifi'] = langBuilder(zh="WiFi信号好驻到VoWiFi", en="Auto Attach to VoWiFi Due to Strong WiFi Signal")

#some error between imscm and telephony
#defined in ImsConnectionManagerService.java
ReportHandoverphrase['switch vowifi'] = dict()
ReportHandoverphrase['switch vowifi'] = langBuilder(zh="Telephony Error: 切换到VoWiFi失败", en="Telephony Error: Failed to handover to VoWiFi")
ReportHandoverphrase['handover vowifi'] = dict()
ReportHandoverphrase['handover vowifi'] = langBuilder(zh="Telephony Error: 电话中切换到VoWiFi失败", en="Telephony Error: Failed to handover to VoWiFi In Call")
ReportHandoverphrase['handover volte'] = dict()
ReportHandoverphrase['handover volte'] = langBuilder(zh="Telephony Error: 电话中切换到VoLTE失败", en="Telephony Error: Failed to handover to VoLTE In Call")
ReportHandoverphrase['handover volte by timer'] = dict()
ReportHandoverphrase['handover volte by timer'] = langBuilder(zh="Telephony Error: 电话中定时器切换到VoLTE失败", en="Telephony Error: Failed to handover to VoLTE by Timer In Call")
ReportHandoverphrase['release vowifi resource'] = dict()
ReportHandoverphrase['release vowifi resource'] = langBuilder(zh="Telephony Error: 释放VoWiFi资源失败", en="Telephony Error: Failed to release vowifi resource")
ReportHandoverphrase['set vowifi unavailable'] = dict()
ReportHandoverphrase['set vowifi unavailable'] = langBuilder(zh="Telephony Error: 关闭VoWiFi失败", en="Telephony Error: Failed to set vowifi unavailable")
ReportHandoverphrase['cancel current request'] = dict()
ReportHandoverphrase['cancel current request'] = langBuilder(zh="Telephony Error: 取消当前请求失败", en="Telephony Error: Failed to cancel current request")
ReportHandoverphrase['videonortp'] = dict()
ReportHandoverphrase['videonortp'] = langBuilder(zh="没有视频数据", en="No RTP in Video")
ReportHandoverphrase['voicenortp'] = dict()
ReportHandoverphrase['voicenortp'] = langBuilder(zh="没有语音数据", en="No RTP in Voice")

ReportScenariophrase = dict()
ReportScenariophrase['startvoltecall'] = dict()
ReportScenariophrase['startvoltecall'] = langBuilder(zh="拨打VoLTE电话", en="Start VoLTE Call")
ReportScenariophrase['startvowificall'] = dict()
ReportScenariophrase['startvowificall'] = langBuilder(zh="拨打VoWiFi电话", en="Start VoWiFi Call")

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


