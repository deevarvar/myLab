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
#      #       6. add catagory to display, top occurence and timestamp (Definition of Done: DoD )
#       6.1 user action,  phone, scenario
#       7. add ho, call, user action

#
#       8. add normal scenarioes details
#       8.1 timestamps, etc
#       8.2 redirect all overview log to overview.log and add a link in html, link to main.pdf
#       10. add datarouter count
#TODO:
#       9. radio log catagory

#       12. process duration: s2b, reg, ho, call
#       12.1 duration
#
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

#FIXME: not easily mapping , add more arg??
def mapzhphrase(key, phrasemap, pre= '',post=''):
    if type(phrasemap) is not dict:
        return key
    if key in phrasemap:
        assembleen = pre + phrasemap[key].geten()+ post
        assemblezh = pre + phrasemap[key].getzh()+ post
        return assembleen + "<br>" + assemblezh
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
ReportHandoverphrase['autowifi'] = langBuilder(zh="WiFi信号好驻网到VoWiFi", en="Auto Attach to VoWiFi Due to Strong WiFi Signal")

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

ReportHandoverphrase['cmendcall'] = dict()
ReportHandoverphrase['cmendcall'] = langBuilder(zh="ImsConnectionManager挂断电话", en="ImsCM hung up call")


ReportScenariophrase = dict()
ReportScenariophrase['startvoltecall'] = dict()
ReportScenariophrase['startvoltecall'] = langBuilder(zh="Telephony拨打VoLTE电话", en="Telephony Start VoLTE Call")
ReportScenariophrase['startvowificall'] = dict()
ReportScenariophrase['startvowificall'] = langBuilder(zh="Telephony拨打VoWiFi电话", en="Telephony Start VoWiFi Call")

ReportScenariophrase['apmakecall'] = dict()
ReportScenariophrase['apmakecall'] = langBuilder(zh="AP Stack拨打VoWiFi电话给", en="AP Stack Start VoWiFi Call to ")

ReportScenariophrase['callfailed'] = dict()
ReportScenariophrase['callfailed'] = langBuilder(zh="拨打VoWiFi电话失败", en="Failed to Start VoWiFi Call")

ReportScenariophrase['unregcallfail'] = dict()
ReportScenariophrase['unregcallfail'] = langBuilder(zh="未注册而拨打VoWiFi电话失败", en="Failed to Start VoWiFi Call Due to Unregistered")

ReportScenariophrase['Voice Call'] = dict()
ReportScenariophrase['Voice Call'] = langBuilder(zh="接听语音电话", en="Answer Voice Call")

ReportScenariophrase['Video Call'] = dict()
ReportScenariophrase['Video Call'] = langBuilder(zh="接听视频电话", en="Answer Video Call")

ReportScenariophrase['rejectcall'] = dict()
ReportScenariophrase['rejectcall'] = langBuilder(zh="拒接电话因为", en="Reject Call As ")

ReportScenariophrase['termcall'] = dict()
ReportScenariophrase['termcall'] = langBuilder(zh="挂断电话因为", en="Term Call As ")

ReportScenariophrase['holdcall'] = dict()
ReportScenariophrase['holdcall'] = langBuilder(zh="保持电话", en="Hold Call")

ReportScenariophrase['resumecall'] = dict()
ReportScenariophrase['resumecall'] = langBuilder(zh="恢复电话", en="Resume Call")

ReportScenariophrase['upgradecall'] = dict()
ReportScenariophrase['upgradecall'] = langBuilder(zh="升级为视频电话", en="Upgrade Video Call")

ReportScenariophrase['downgradecall'] = dict()
ReportScenariophrase['downgradecall'] = langBuilder(zh="降级为语音电话", en="Downgrade Voice Call")

ReportScenariophrase['mdyfailed'] = dict()
ReportScenariophrase['mdyfailed'] = langBuilder(zh="升级/降级失败", en="Failed to Upgrade/Downgrade Call")

ReportScenariophrase['akaok'] = dict()
ReportScenariophrase['akaok'] = langBuilder(zh="EAP-AKA校验成功", en="EAP-AKA AUTH correctly")

ReportScenariophrase['akafailed'] = dict()
ReportScenariophrase['akafailed'] = langBuilder(zh="EAP-AKA校验SYNC失败", en="EAP-AKA AUTH SYNC Failure")

ReportScenariophrase['akafailed'] = dict()
ReportScenariophrase['akafailed'] = langBuilder(zh="EAP-AKA校验SYNC失败", en="EAP-AKA AUTH SYNC Failure")

ReportScenariophrase['sendsms'] = dict()
ReportScenariophrase['sendsms'] = langBuilder(zh="发送SMS Over IP", en="Send SMS Over IP")

ReportScenariophrase['sendsmsok'] = dict()
ReportScenariophrase['sendsmsok'] = langBuilder(zh="发送SMS Over IP成功,类型:", en="Send SMS Over IP OK,type:")

ReportScenariophrase['recvsms'] = dict()
ReportScenariophrase['recvsms'] = langBuilder(zh="接收到SMS Over IP", en="Recv SMS Over IP")

ReportScenariophrase['sendsmsack'] = dict()
ReportScenariophrase['sendsmsack'] = langBuilder(zh="发送SMS ACK", en="Send SMS ACK")

ReportScenariophrase['sendsmsack'] = dict()
ReportScenariophrase['sendsmsack'] = langBuilder(zh="发送SMS ACK", en="Send SMS ACK")

ReportScenariophrase['sendsmsfailed'] = dict()
ReportScenariophrase['sendsmsfailed'] = langBuilder(zh="发送SMS失败, 类型:", en="Failed to send SMS, type:")

ReportScenariophrase['sendsmstimeout'] = dict()
ReportScenariophrase['sendsmstimeout'] = langBuilder(zh="发送SMS超时", en="Send SMS timeout")

ReportScenariophrase['pingfail'] = dict()
ReportScenariophrase['pingfail'] = langBuilder(zh="驻网ping失败", en="ping failed when ePDG attach")

ReportScenariophrase['wpaselect'] = dict()
ReportScenariophrase['wpaselect'] = langBuilder(zh="选择新的WiFi AP:", en="Select New WiFi AP:")
#drstatus
ReportScenariophrase['drstatus'] = dict()
ReportScenariophrase['drstatus'] = langBuilder(zh="更新数据路由到", en="Update data router to ")

#various servicecallback phrase
ReportScenariophrase["call_incoming"] = dict()
ReportScenariophrase["call_incoming"] = langBuilder(zh="收到来电", en="Receive incoming Call")

ReportScenariophrase["call_talking"] = dict()
ReportScenariophrase["call_talking"] = langBuilder(zh="电话接通", en="Call is established")

ReportScenariophrase["call_hold_ok"] = dict()
ReportScenariophrase["call_hold_ok"] = langBuilder(zh="电话保持成功", en="Call hold successfully")

ReportScenariophrase["call_resume_ok"] = dict()
ReportScenariophrase["call_resume_ok"] = langBuilder(zh="电话恢复成功", en="Call resume successfully")

ReportScenariophrase["call_hold_received"] = dict()
ReportScenariophrase["call_hold_received"] = langBuilder(zh="被对方保持电话", en="Call is held by peer")

ReportScenariophrase["call_resume_received"] = dict()
ReportScenariophrase["call_resume_received"] = langBuilder(zh="被对方恢复电话", en="Call is resumed by peer")

ReportScenariophrase["call_add_video_ok"] = dict()
ReportScenariophrase["call_add_video_ok"] = langBuilder(zh="添加视频成功", en="Add Video OK")

ReportScenariophrase["call_remove_video_ok"] = dict()
ReportScenariophrase["call_remove_video_ok"] = langBuilder(zh="移除视频成功", en="Remove Video OK")

ReportScenariophrase["call_remove_video_ok"] = dict()
ReportScenariophrase["call_remove_video_ok"] = langBuilder(zh="移除视频成功", en="Remove Video OK")

ReportScenariophrase["call_add_video_request"] = dict()
ReportScenariophrase["call_add_video_request"] = langBuilder(zh="收到添加视频的请求", en="Receive add video request")

ReportScenariophrase["call_add_video_cancel"] = dict()
ReportScenariophrase["call_add_video_cancel"] = langBuilder(zh="收到取消添加视频的请求", en="Receive request to cancel add video")

ReportScenariophrase["conf_connected"] = dict()
ReportScenariophrase["conf_connected"] = langBuilder(zh="会议电话建立", en="Conference Call is established")

ReportScenariophrase["conf_disconnected"] = dict()
ReportScenariophrase["conf_disconnected"] = langBuilder(zh="会议电话结束", en="Conference Call is disconnedted")

ReportScenariophrase["conf_invite_accept"] = dict()
ReportScenariophrase["conf_invite_accept"] = langBuilder(zh="对方接受会议电话", en="Peer accept Conference Call")

ReportScenariophrase["conf_kick_accept"] = dict()
ReportScenariophrase["conf_kick_accept"] = langBuilder(zh="移除会议参加者", en="Kick Peer from Conference Call")

ReportScenariophrase["conf_part_update"] = dict()
ReportScenariophrase["conf_part_update"] = langBuilder(zh="会议参加者状态更新", en="Conf Peer state updated")

ReportScenariophrase["conf_hold_ok"] = dict()
ReportScenariophrase["conf_hold_ok"] = langBuilder(zh="会议电话保持成功", en="Conference Call hold successfully")

ReportScenariophrase["conf_resume_ok"] = dict()
ReportScenariophrase["conf_resume_ok"] = langBuilder(zh="会议电话恢复成功", en="Conference Call resume successfully")

ReportScenariophrase["conf_hold_received"] = dict()
ReportScenariophrase["conf_hold_received"] = langBuilder(zh="被对方保持会议电话", en="Conference Call is held by peer")

ReportScenariophrase["conf_resume_received"] = dict()
ReportScenariophrase["conf_resume_received"] = langBuilder(zh="被对方恢复会议电话", en="Conference Call is resumed by peer")

ReportScenariophrase["call_hold_failed"] = dict()
ReportScenariophrase["call_hold_failed"] = langBuilder(zh="电话保持失败", en="Failed to hold call")

ReportScenariophrase["call_resume_failed"] = dict()
ReportScenariophrase["call_resume_failed"] = langBuilder(zh="电话恢复失败", en="Failed to resume call")

ReportScenariophrase["call_add_video_failed"] = dict()
ReportScenariophrase["call_add_video_failed"] = langBuilder(zh="添加视频失败", en="Failed to add video to call")

ReportScenariophrase["call_remove_video_failed"] = dict()
ReportScenariophrase["call_remove_video_failed"] = langBuilder(zh="移除视频失败", en="Failed to remove video from call")

ReportScenariophrase["conf_invite_failed"] = dict()
ReportScenariophrase["conf_invite_failed"] = langBuilder(zh="会议电话失败", en="Failed to start Conference call")

ReportScenariophrase["conf_kick_failed"] = dict()
ReportScenariophrase["conf_kick_failed"] = langBuilder(zh="会议电话移除参与者失败", en="Failed to kick peer from Conference call")

ReportScenariophrase["conf_hold_failed"] = dict()
ReportScenariophrase["conf_hold_failed"] = langBuilder(zh="会议电话保持失败", en="Failed to hold Conference call")

ReportScenariophrase["conf_resume_failed"] = dict()
ReportScenariophrase["conf_resume_failed"] = langBuilder(zh="会议电话恢复失败", en="Failed to resume Conference call")



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


