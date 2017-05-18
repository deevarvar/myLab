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
#      8.1.2 imscm operation result
#        OPERATION_SWITCH_TO_VOWIFI, OPERATION_SWITCH_TO_VOLTE,...... defined in ImsConnectionMangerConstants.java
#      8.1.3 wpa_supplicant: wlan0: State: ASSOCIATED -> COMPLETED
#       8.3 datarouter error
#        D:\code\log\bug_log\vit_log\2017_3_2\wificalling_no_Voice_video_1082#0310a
#        [Adapter]VoWifiCallManager: Failed to update the data router state, please check
#         imscm Currently used IMS protocol stack: "VoLte IMS protocol stack"
#      8.1.4 cp color, green, volte failed
#     D:\code\log\bug_log\vit_log\2017_3_24\659070\Handover_to_VoLTE_Calldrop_2238\external_storage\ylog\ylog
#        8.1.5 504 timeout
#        ImsReasonInfo.java, more definition
#        D:\code\log\srvcc\wei_504
# 03-27 15:10:06.227  1134  1134 I [VoWifiService]VoWifiSerService: Notify the event: {"event_code":105,"event_name":"call_terminate","id":1,"state_code":146}
#         D:\code\log\srvcc\503\slog_20170327151140_sp9832a_2h11_4mvolt_vowif_userdebu\external_storage\ylog\ylog
#     8.1.6 ap color, servicecallback : talking, ok should be green
#       8.1.7 srvcc report
#      8.1.8 call_terminate report
#       9. radio log catagory
#       9.1 FIXME: add at cmd result , log is too verboses....
#           D:\code\iwhale2\log\cp_reject
#       self.atmsgs, add field
#     8.1.9  search pattern , add logic to handle subprocess

#     8.1.11 ImsCM code changed.
#       #temporary add some logs.
#      1. card is not enabled.
#      2. audioqos: D:\code\log\bug_log\vit_log\2017_3_24\659089\ylog

##    8.1.12  ims code ACTION_SWITCH_IMS_FEATURE,
#     , add
#     aidl: vendor/sprd/platform/frameworks/
#     case:
#          1. EVENT_WIFI_ATTACH_SUCCESSED, EVENT_WIFI_ATTACH_FAILED, ACTION_NOTIFY_VOWIFI_UNAVAILABLE
#          2. ImsService: Needn't switch to type 2 as it already registed.
#          3. OPERATION_HANDOVER_TO_VOWIFI in ImsCM is the same in tele's IMS_OPERATION_HANDOVER_TO_VOWIFI
#          4. tele's log.w, log.e
#D:\code\log\ref_log\instruments\Anritsu\call_scenarioes\merge_test\log4
#http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=663113
#http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=659089
#D:\code\log\bug_log\vit_log\2017_3_24\659089\ylog
#      8.1.3.4 new imscm : D:\code\log\ref_log\EE\poweroff_dereg
#      8.1.3.1 REGISTER display add backward option for searchsip
##     8.1.3.3 new s2b code C:\Users\Zhihua.Ye\Documents\MyJabberFiles\yingying.fan@spreadtrum.com\s2b_new\ylog\
#     8.1.10 onLoginFinished
#D:\code\log\bug_log\vit_log\2017_3_24\660071\ylog
#   8.1.3  log more
#         1. 01-01 09:18:14.321  1140  2496 I CPVoiceAgent: [cp_mediaset]: AT+SPRTPMEDIASET=3,1,1,1
#         2. DSCI D:\code\log\bug_log\vit_log\2017_4_14\660061\ylog2

##   new ho no rtp
#  8.2.0 add calling mode
#  Wifi-calling mode is "Cellular preferred"
#   8.2.a.3  CEREG add too verbose, FIXME: not to added

#   8.2.a    pcscf passing
#   8.2.a.1 ap to cp: AT+VOWIFIPCSCF
#Parameter:
#< type>: 0, FQDN
#        1, IPV4
#        2, IPV6
#<addr> string
#       AT+VOWIFIPCSCF=1,"10.15.0.26"
#   8.2.a.2 cp to ap: ImsServiceImpl: getImsPcscfAddress mImsPscfAddress = \\10.0.0.166\Logs\From_Taipei\Taipei_Logs\VoWiFiPowerTest\Indonisa\0503
#    D:\code\log\ref_log\smartfren\smart_volte_idle_ho_vowifi\android
#    full function open, error grep
#    D:\code\merge\isharkl2 do_ip failed
#    add zxsocket grep...
##   8.2.a.4 parse tw logs failed, no sip D:\code\merge\tw\672534\volte_ho_vowifi
#    8.0.111 Authentication: Failed to get the challenge response. D:\code\so\juphoonlib\develop\7lib\sos\1
#    8.2.00  imscm ho stragtegy

#   new imscm logs D:\code\merge\dtac
#   1. createPolicyTimerTask: don't create timer task during Vowifi and 2/3G or UNKNOWN network
#   add all task "Conditions are not satisfied" , warning
#    D:\code\merge\indonisia\can'tregistervowifi2\ylog\android
#   8.3 add pending warning, s2b not return
#  D:\code\log\bug_log\vit_log\2017_4_14\668339\ylog
#   handleMessageSwitchToVowifi: "MSG_SWITCH_TO_VOWIFI", mCurPendingMsgId = "MSG_RELEASE_VOWIFI_RES",

#TODO:

#    8.0 simplify error output.
#     eventname/timestamp in html is not correct
#
#    7.9 emergency call
#    8.1.99 save some json file

#   8.2.b optimize lemonlog in flowParser.py
#   8.2.02 onsrvccfailed http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=666546
#   8.2.002 deactive-pdn failed http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=673148
#   8.2.01  D:\code\log\ref_log\instruments\sprient\newversion2\nonce_null
#   1. add error:Can not get data from the nonce as it is null
#   2. impu, impi
#   3. crash log findings
#    native crash :  D:\code\log\ref_log\instruments\sprient\newversion2\nonce_null
#       04-15 16:28:38.234  6114  6114 F DEBUG   : pid: 4663, tid: 4686, name: Thread-4  >>> com.sprd.vowifi.security <<<
#    app crash:      D:\code\log\bug_log\vit_log\2017_4_14\665551\vowifiservice\log_sp9861e_1h10_vm_userdebu\external_storage\ylog
#       04-13 19:53:25.953  3814  3814 E AndroidRuntime: Process: com.spreadtrum.vowifi, PID: 3814


# D:\code\log\bug_log\vit_log\2017_4_14\piclab_4_17\HO_connection\ylog
#   8.2.1 ImcM Qos
#    http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=666173
#   8.2.2 call optimization
#    add call number D:\code\log\bug_log\vit_log\2017_4_14\665355
#   8.2.3 more media AT parsing., SPRTPCHANNEL
#   CPVoiceAgent: AT> AT+SPRTPCHANNEL="01018D9009AA8C9008AA010A0F200600000000000000000000000001647CDFCB000000000000000000000000"

#
#      8.1.3.2 new ike error code
#      high prio

#       1. display flag on handler
#      8.1.4 D:\code\log\ref_log\instruments\Anritsu\error_sample  error sample
#     8.1.4.1 add crash report
#     8.1.12 rssi, Qos jquery chart.


#     8.1.13 dialer
#          CallCardPresenter.java, CallButtonPresenter.java
#    add more decode about call and profile
# InCall  : CallCardPresenter - Disconnecting call: [Call_2, ACTIVE, [Capabilities: CAPABILITY_HOLD CAPABILITY_SUPPORT_HOLD CAPABILITY_MUTE CAPABILITY_SUPPORTS_VT_LOCAL_RX CAPABILITY_SUPPORTS_VT_LOCAL_TX CAPABILITY_SUPPORTS_VT_LOCAL_BIDIRECTIONAL CAPABILITY_SUPPORTS_VT_REMOTE_RX CAPABILITY_SUPPORTS_VT_REMOTE_TX CAPABILITY_SUPPORTS_VT_REMOTE_BIDIRECTIONAL CAPABILITY_CAN_PAUSE_VIDEO], children:[], parent:null, conferenceable:[], videoState:Audio Only, mSessionModificationState:0, VideoSettings:(CameraDir:-1)
#    packages/apps/Dialer/InCallUI/src/com/android/incallui
#    from callcard to try the call duration
#


#     8.2.0 http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=659089
#      my comments
#       8.2.1 call session
#       event.log /main.pdf diffs
#      8.2.3 all success/failed event, only care about handover, register,call
#      handover errors:
#      volte register fail: D:\code\log\bug_log\vit_log\2017_3_24\659089\13slog_20170325222251_sp9832a_2h11_ho_VoWIFI_dropcall_2220-2222\external_storage\ylog
#      vowifi register faile: D:\code\log\bug_log\vit_log\2017_4_1\spirent_rereg\ylog
#      s2b failed: D:\code\log\bug_log\vit_log\2017_4_14\666137\ylog1\
#
#      8.2.4 owner display : too aggressive

#      8.2.300 regstatus add refresh failed

#https://SHTEMP832PC.spreadtrum.com:444/svn/Vowifi_Log_Tool/
#log tool
#一般人就用user账户下载，不需要密码
#你用admin:admin上传
#renlong.he 2296206

#
# 8.1.100 ipsec cmd
#
#
#       9.2 add CPVoiceAgent 's at parsing
#           D:\code\log\bug_log\vit_log\2017_3_2\con_call
#       at cmd
#       9.3 ringtone
#
#

#       10.0  g_astMtcCliCodeMap , g_astMtcCallCodeMap

#       10. add imsservice logic
#            onReceiveHandoverEvent, onImsHandoverStateChange,onImsPdnStatusChange,
#       imscm's logic  : "imsServiceEx"
#       add timing calcute
#       15. outgoing, alerting
#       16. more bugs to analyze
#       16.1 imswaitvoltereg D:\code\log\bug_log\vit_log\2017_2_14\644337\Fail_S2b_Attach_Data_OK_No_error_popup\AP\ylog
#
#       wifi call end with volte call ,volte not reg. , IMSEN=1 not send
#       try vowifi call ,ho to volte, end call ,if reg to volte
#       16.1.1 D:\code\iwhale2\log\cp_reject ho cp reject
#       16.2 imscmopfailed  D:\code\log\bug_log\vit_log\2017_2_14\644735\IDLE_1\slog_20170217133643_sp9832a_2h11_4mvoltesea_userdebug\external_storage\ylog\ylog
#       16.3 imscallend http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=645833
#       16.4 conf scenario:  http://bugzilla.spreadtrum.com/bugzilla/show_bug.cgi?id=646232
#       16.5 camera D:\code\log\bug_log\vit_log\2017_2_14\644983\vowifi_Active Video + MT Alerting Video\1\2\external_storage\ylog\ylog
#        Set the camera to
#        16.6 sim card not support vowifi:  D:\code\so\juphoonlib\develop\6lib\lib\sim_not_support
#        setCheckWifiConnectivityState: not found plmn in mAllPlmnArrayList and not Lab's card
#
#        add report
#       17. predict:
#       17.1 wifi conn
#       17.2 callid, call state match, incoming ,talking...
#       17.3 idle ho , ho in call
#       17.3 stack state
#       17.3 module owner, doc update
#       17.8 ho success: epdg, pdn, etc
#       17.9 call term by user/network
#       18. supplementary service

#       12. process duration: s2b, reg, ho, call
#       12.1 duration
#       13 tracing log should be deleted.
#       14. chinese name path

# ppt prepare:
#   1. scenarioes: D:\code\log\bug_log\vit_log\2017_4_14\668542


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
        if phrasemap[key].getzh():
            assemblezh = pre + phrasemap[key].getzh()+ post
        else:
            assemblezh = ''
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
ReportHandoverphrase['wificonn'] = langBuilder(zh="ImsCM 连上WiFi", en="ImsCM WiFi is Connected")

ReportHandoverphrase['wifidisconn'] = dict()
ReportHandoverphrase['wifidisconn'] = langBuilder(zh="ImsCM WiFi断开连接", en="ImsCM WiFi is Disconnected")


ReportHandoverphrase['airon'] = dict()
ReportHandoverphrase['airon'] = langBuilder(zh="打开飞行模式", en="open airplane mode")


ReportHandoverphrase['airoff'] = dict()
ReportHandoverphrase['airoff'] = langBuilder(zh="关闭飞行模式", en="close airplane mode")

ReportHandoverphrase['enwfc'] = dict()
ReportHandoverphrase['enwfc'] = langBuilder(zh="打开WiFi-Calling", en="Enable WiFi-Calling")

ReportHandoverphrase['disenwfc'] = dict()
ReportHandoverphrase['disenwfc'] = langBuilder(zh="关闭WiFi-Calling", en="Disable WiFi-Calling")

ReportHandoverphrase['invalidsim'] = dict()
ReportHandoverphrase['invalidsim'] = langBuilder(zh="Sim卡不在白名单，禁用VoWiFi", en="SimCard is not in VoWiFi whitelist")

ReportHandoverphrase['idlehowifi'] = dict()
ReportHandoverphrase['idlehowifi'] = langBuilder(zh="尝试Idle切换到VoWiFi", en="Trying to Idle Handover to VoWiFi")
ReportHandoverphrase['idleholte'] = dict()
ReportHandoverphrase['idleholte'] = langBuilder(zh="尝试Idle切换到VoLTE", en="Trying to Idle Handover to VoLTE")
ReportHandoverphrase['callhowifi'] = dict()
ReportHandoverphrase['callhowifi'] = langBuilder(zh="尝试电话中切到VoWiFi", en="Trying to Handover to VoWiFi in Call")
ReportHandoverphrase['callholte'] = dict()
ReportHandoverphrase['callholte'] = langBuilder(zh="尝试电话中切到VoLTE", en="Trying to Handover to VoLTE in Call")
ReportHandoverphrase['voiceqos2lte'] = dict()
ReportHandoverphrase['voiceqos2lte'] = langBuilder(zh="尝试语音通话质量差切换到Volte", en="Trying to Handover to VoLTE Due to Poor Voice Quality")
ReportHandoverphrase['videoqos2lte'] = dict()
ReportHandoverphrase['videoqos2lte'] = langBuilder(zh="尝试视频通话质量差切换到Volte", en="Trying to Handover to VoLTE Due to Poor Video Quality")

ReportHandoverphrase['incallrssiho2wifi'] = dict()
ReportHandoverphrase['incallrssiho2wifi'] = langBuilder(zh="尝试通话中WiFi信号好切换到VoWiFi", en="Trying to Handover to VoWiFi In Call Due to Strong WiFi Signal")

ReportHandoverphrase['rssiho2wifi'] = dict()
ReportHandoverphrase['rssiho2wifi'] = langBuilder(zh="尝试WiFi信号好切换到VoWiFi", en="Trying to Handover to VoWiFi From VoLTE Due to Strong WiFi Signal")

ReportHandoverphrase['autowifi'] = dict()
ReportHandoverphrase['autowifi'] = langBuilder(zh="尝试WiFi信号好驻网到VoWiFi", en="Trying to Auto Attach to VoWiFi Due to Strong WiFi Signal")

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

#OPERATION_SWITCH_TO_VOWIFI
ReportHandoverphrase['OPERATION_SWITCH_TO_VOWIFI'] = dict()
ReportHandoverphrase['OPERATION_SWITCH_TO_VOWIFI'] = langBuilder(en="Idle Handover to VoWiFi ")
#OPERATION_SWITCH_TO_VOLTE
ReportHandoverphrase['OPERATION_SWITCH_TO_VOLTE'] = dict()
ReportHandoverphrase['OPERATION_SWITCH_TO_VOLTE'] = langBuilder(en="Idle Handover to VoLTE ")
#OPERATION_HANDOVER_TO_VOWIFI
ReportHandoverphrase['OPERATION_HANDOVER_TO_VOWIFI'] = dict()
ReportHandoverphrase['OPERATION_HANDOVER_TO_VOWIFI'] = langBuilder(en="Handover to VoWiFi in Call ")

#OPERATION_HANDOVER_TO_VOLTE
ReportHandoverphrase['OPERATION_HANDOVER_TO_VOLTE'] = dict()
ReportHandoverphrase['OPERATION_HANDOVER_TO_VOLTE'] = langBuilder(en="Handover to VoLTE in Call ")

#OPERATION_SET_VOWIFI_UNAVAILABLE
ReportHandoverphrase['OPERATION_SET_VOWIFI_UNAVAILABLE'] = dict()
ReportHandoverphrase['OPERATION_SET_VOWIFI_UNAVAILABLE'] = langBuilder(en="Stop VoWiFi Stack ")

#OPERATION_CANCEL_CURRENT_REQUEST
ReportHandoverphrase['OPERATION_CANCEL_CURRENT_REQUEST'] = dict()
ReportHandoverphrase['OPERATION_CANCEL_CURRENT_REQUEST'] = langBuilder(en="ImsCM Cancel Current Request ")

#OPERATION_CP_REJECT_SWITCH_TO_VOWIFI
ReportHandoverphrase['OPERATION_CP_REJECT_SWITCH_TO_VOWIFI'] = dict()
ReportHandoverphrase['OPERATION_CP_REJECT_SWITCH_TO_VOWIFI'] = langBuilder(en="CP Reject to Idle Handover to VoWiFi ")


#OPERATION_CP_REJECT_HANDOVER_TO_VOWIFI
ReportHandoverphrase['OPERATION_CP_REJECT_HANDOVER_TO_VOWIFI'] = dict()
ReportHandoverphrase['OPERATION_CP_REJECT_HANDOVER_TO_VOWIFI'] = langBuilder(en="CP Reject to Handover to VoWiFi In Call ")

#OPERATION_RELEASE_WIFI_RESOURCE
ReportHandoverphrase['OPERATION_RELEASE_WIFI_RESOURCE'] = dict()
ReportHandoverphrase['OPERATION_RELEASE_WIFI_RESOURCE'] = langBuilder(en="Release VoWiFi Resource ")

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

ReportScenariophrase['wpaconn'] = dict()
ReportScenariophrase['wpaconn'] = langBuilder(zh="WCN 连接上WiFi AP", en="WCN Connected to WiFi AP")

#drstatus
ReportScenariophrase['drstatus'] = dict()
ReportScenariophrase['drstatus'] = langBuilder(zh="更新数据路由到", en="Update data router to ")

#various servicecallback phrase
ReportScenariophrase["call_alert"] = dict()
ReportScenariophrase["call_alert"] = langBuilder(zh="收到18x: ", en="User Alert: ")



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

ReportScenariophrase["conf_outgoing"] = dict()
ReportScenariophrase["conf_outgoing"] = langBuilder(zh="播出会议电话", en="Conf Call Outgoing")

ReportScenariophrase["call_outgoing"] = dict()
ReportScenariophrase["call_outgoing"] = langBuilder(zh="播出电话", en="Call Outgoing")

ReportScenariophrase["voicecallrtp"] = dict()
ReportScenariophrase["voicecallrtp"] = langBuilder(zh="电话收到语音", en="Voice RTP Received")
ReportScenariophrase["videocallrtp"] = dict()
ReportScenariophrase["videocallrtp"] = langBuilder(zh="电话收到视频", en="Video RTP Received")

ReportScenariophrase["voiceconfrtp"] = dict()
ReportScenariophrase["voiceconfrtp"] = langBuilder(zh="会议电话收到语音", en="Conf Voice RTP Received")
ReportScenariophrase["videoconfrtp"] = dict()
ReportScenariophrase["videoconfrtp"] = langBuilder(zh="会议电话收到视频", en="Conf Video RTP Received")

ReportScenariophrase["voicecallnortp"] = dict()
ReportScenariophrase["voicecallnortp"] = langBuilder(zh="电话没收到语音", en="No Voice RTP Received")
ReportScenariophrase["videocallnortp"] = dict()
ReportScenariophrase["videocallnortp"] = langBuilder(zh="电话没收到视频", en="No Video RTP Received")

ReportScenariophrase["voiceconfnortp"] = dict()
ReportScenariophrase["voiceconfnortp"] = langBuilder(zh="会议电话没收到语音", en="No Conf Voice RTP Received")

ReportScenariophrase["videoconfnortp"] = dict()
ReportScenariophrase["videoconfnortp"] = langBuilder(zh="会议电话没收到视频", en="No Conf Video RTP Received")

ReportScenariophrase["adddrerror"] = dict()
ReportScenariophrase["adddrerror"] = langBuilder(en="Failed to Update DataRouter")

ReportScenariophrase["call_terminate"] = dict()
ReportScenariophrase["call_terminate"] = langBuilder(zh="电话挂断因为 ", en="TermCall As ")

ReportScenariophrase["nonceerror"] = dict()
ReportScenariophrase["nonceerror"] = langBuilder(zh="服务器没回复nonce值", en="Auth Nonce is null")

ReportScenariophrase["akaerror"] = dict()
ReportScenariophrase["akaerror"] = langBuilder(zh="AKA计算失败", en="Failed to Caculate AKA response.")

ReportCpphrase = dict()
ReportCpphrase["PDN connection established"] = dict()
ReportCpphrase["PDN connection established"] = langBuilder(zh="PDN激活", en="PDN connection established")

ReportCpphrase["PDN connection request"] = dict()
ReportCpphrase["PDN connection request"] = langBuilder(zh="发起PDN请求", en="PDN connection request")

ReportCpphrase["Deactivate PDN connection"] = dict()
ReportCpphrase["Deactivate PDN connection"] = langBuilder(zh="PDN去激活", en="Deactivate PDN connection")

ReportCpphrase["VoLTE Unregistered"] = dict()
ReportCpphrase["VoLTE Unregistered"] = langBuilder(zh="VoLTE去注册", en="VoLTE Unregistered")

ReportCpphrase["VoLTE Registered"] = dict()
ReportCpphrase["VoLTE Registered"] = langBuilder(zh="VoLTE注册成功", en="VoLTE Registeredd")

ReportCpphrase["VoLTE Register fail"] = dict()
ReportCpphrase["VoLTE Register fail"] = langBuilder(zh="VoLTE注册失败", en="VoLTE Register fail")

ReportCpphrase["VoLTE De-Registering"] = dict()
ReportCpphrase["VoLTE De-Registering"] = langBuilder(zh="VoLTE正在去注册", en="VoLTE De-Registering")

ReportCpphrase["No RTP data!"] = dict()
ReportCpphrase["No RTP data!"] = langBuilder(en="No RTP data!")

ReportCpphrase["Enable VoLTE IMS"] = dict()
ReportCpphrase["Enable VoLTE IMS"] = langBuilder(en="Enable VoLTE IMS")

ReportCpphrase["PS to CS SRVCC Started"] = dict()
ReportCpphrase["PS to CS SRVCC Started"] = langBuilder(zh="SRVCC开始", en="SRVCC Started")

ReportCpphrase["PS to CS SRVCC Successfully"] = dict()
ReportCpphrase["PS to CS SRVCC Successfully"] = langBuilder(zh="SRVCC成功", en="SRVCC Successfully")

ReportCpphrase["PS to CS SRVCC Cancelled"] = dict()
ReportCpphrase["PS to CS SRVCC Cancelled"] = langBuilder(zh="SRVCC取消", en="SRVCC Cancelled")

ReportCpphrase["PS to CS SRVCC Failed"] = dict()
ReportCpphrase["PS to CS SRVCC Failed"] = langBuilder(zh="SRVCC失败", en="SRVCC Failed")

ReportTelphrase = dict()
ReportTelphrase['attachexception'] = dict()
ReportTelphrase['attachexception'] = langBuilder(zh="手动点击S2b驻网", en="Start S2b Attach without switch request")

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
#FIXME: for this file, the msg should be arranged in a good way.

