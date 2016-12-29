#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

Q850map = dict()

Q850map['1'] = dict()
Q850map['1']['isdn'] = "unallocated number"
Q850map['1']['sip'] = "404 Not found"

Q850map['2'] = dict()
Q850map['2']['isdn'] = "no route to network"
Q850map['2']['sip'] = "404 Not found"

Q850map['3'] = dict()
Q850map['3']['isdn'] = "no route to destination"
Q850map['3']['sip'] = "404 Not found"

Q850map['6'] = dict()
Q850map['6']['isdn'] = "CHANNEL_UNACCEPTABLE"
Q850map['6']['sip'] = ""

Q850map['7'] = dict()
Q850map['7']['isdn'] = "CALL_AWARDED_DELIVERED"
Q850map['7']['sip'] = ""

Q850map['16'] = dict()
Q850map['16']['isdn'] = "NORMAL_CLEARING"
Q850map['16']['sip'] = ""

Q850map['17'] = dict()
Q850map['17']['isdn'] = "17 user busy"
Q850map['17']['sip'] = "486 Busy here"

Q850map['18'] = dict()
Q850map['18']['isdn'] = "no user responding"
Q850map['18']['sip'] = "408 Request Timeout"

Q850map['19'] = dict()
Q850map['19']['isdn'] = "no answer from the user"
Q850map['19']['sip'] = "480 Temporarily unavailable"

Q850map['20'] = dict()
Q850map['20']['isdn'] = "subscriber absent"
Q850map['20']['sip'] = "480 Temporarily unavailable"

Q850map['21'] = dict()
Q850map['21']['isdn'] = "call rejected"
Q850map['21']['sip'] = "603 Decline"


Q850map['22'] = dict()
Q850map['22']['isdn'] = "number changed"
Q850map['22']['sip'] = "410 Gone"

Q850map['23'] = dict()
Q850map['23']['isdn'] = "redirection to new destination"
Q850map['23']['sip'] = "410 Gone"


Q850map['25'] = dict()
Q850map['25']['isdn'] = "EXCHANGE_ROUTING_ERRORn"
Q850map['25']['sip'] = "483 Too Many Hops"

Q850map['26'] = dict()
Q850map['26']['isdn'] = "non-selected user clearing"
Q850map['26']['sip'] = "404 Not Found"

Q850map['27'] = dict()
Q850map['27']['isdn'] = "destination out of order"
Q850map['27']['sip'] = "502 Bad Gateway"

Q850map['28'] = dict()
Q850map['28']['isdn'] = "address incomplete"
Q850map['28']['sip'] = "484 Address incomplete"

Q850map['29'] = dict()
Q850map['29']['isdn'] = "facility rejected"
Q850map['29']['sip'] = "501 Not implemented"

Q850map['30'] = dict()
Q850map['30']['isdn'] = "RESPONSE_TO_STATUS_ENQUIRY"
Q850map['30']['sip'] = ""

Q850map['31'] = dict()
Q850map['31']['isdn'] = "normal unspecified"
Q850map['31']['sip'] = "480 Temporarily unavailable"

Q850map['34'] = dict()
Q850map['34']['isdn'] = "no circuit available"
Q850map['34']['sip'] = "503 Service unavailable"

Q850map['38'] = dict()
Q850map['38']['isdn'] = "network out of order"
Q850map['38']['sip'] = "503 Service unavailable"

Q850map['41'] = dict()
Q850map['41']['isdn'] = "temporary failure"
Q850map['41']['sip'] = "503 Service unavailable"

Q850map['42'] = dict()
Q850map['42']['isdn'] = "switching equipment congestion"
Q850map['42']['sip'] = "503 Service unavailable"

Q850map['43'] = dict()
Q850map['43']['isdn'] = "ACCESS_INFO_DISCARDED"
Q850map['43']['sip'] = ""

Q850map['44'] = dict()
Q850map['44']['isdn'] = "REQUESTED_CHAN_UNAVAIL"
Q850map['44']['sip'] = "503 Service unavailable"

Q850map['45'] = dict()
Q850map['45']['isdn'] = "PRE_EMPTED"
Q850map['45']['sip'] = ""

Q850map['47'] = dict()
Q850map['47']['isdn'] = "resource unavailable"
Q850map['47']['sip'] = "503 Service unavailable"

Q850map['50'] = dict()
Q850map['50']['isdn'] = "FACILITY_NOT_SUBSCRIBED"
Q850map['50']['sip'] = ""

Q850map['52'] = dict()
Q850map['52']['isdn'] = "OUTGOING_CALL_BARRED"
Q850map['52']['sip'] = "403 Forbidden"


Q850map['54'] = dict()
Q850map['54']['isdn'] = "incoming calls barred"
Q850map['54']['sip'] = "403 Forbidden"

Q850map['57'] = dict()
Q850map['57']['isdn'] = "bearer capability not authorized"
Q850map['57']['sip'] = "403 Forbidden"

Q850map['58'] = dict()
Q850map['58']['isdn'] = "BEARERCAPABILITY_NOTAVAIL"
Q850map['58']['sip'] = "503 Service unavailable"

Q850map['65'] = dict()
Q850map['65']['isdn'] = "BEARERCAPABILITY_NOTIMPL"
Q850map['65']['sip'] = "488 Not Acceptable Here"

Q850map['66'] = dict()
Q850map['66']['isdn'] = "CHAN_NOT_IMPLEMENTED"
Q850map['66']['sip'] = ""

Q850map['69'] = dict()
Q850map['69']['isdn'] = "FACILITY_NOT_IMPLEMENTED"
Q850map['69']['sip'] = "501 Not implemented"

Q850map['70'] = dict()
Q850map['70']['isdn'] = "only restricted digital available"
Q850map['70']['sip'] = "488 Not Acceptable Here"

Q850map['79'] = dict()
Q850map['79']['isdn'] = "SERVICE_NOT_IMPLEMENTED"
Q850map['79']['sip'] = "501 Not implemented"


Q850map['81'] = dict()
Q850map['81']['isdn'] = "INVALID_CALL_REFERENCE"
Q850map['81']['sip'] = ""

Q850map['87'] = dict()
Q850map['87']['isdn'] = "user not member of CUG"
Q850map['87']['sip'] = "403 Forbidden"

Q850map['88'] = dict()
Q850map['88']['isdn'] = "incompatible destination"
Q850map['88']['sip'] = "503 Service unavailable"

Q850map['95'] = dict()
Q850map['95']['isdn'] = "INVALID_MSG_UNSPECIFIED"
Q850map['95']['sip'] = ""

Q850map['96'] = dict()
Q850map['96']['isdn'] = "MANDATORY_IE_MISSING"
Q850map['96']['sip'] = ""

Q850map['97'] = dict()
Q850map['97']['isdn'] = "MESSAGE_TYPE_NONEXIST"
Q850map['97']['sip'] = ""

Q850map['98'] = dict()
Q850map['98']['isdn'] = "WRONG_MESSAGE"
Q850map['98']['sip'] = ""

Q850map['100'] = dict()
Q850map['100']['isdn'] = "INVALID_IE_CONTENTS"
Q850map['100']['sip'] = ""

Q850map['101'] = dict()
Q850map['101']['isdn'] = "WRONG_CALL_STATE"
Q850map['101']['sip'] = ""

Q850map['103'] = dict()
Q850map['103']['isdn'] = "MANDATORY_IE_LENGTH_ERROR"
Q850map['103']['sip'] = ""

Q850map['102'] = dict()
Q850map['102']['isdn'] = "recovery of timer expiry"
Q850map['102']['sip'] = "504 Gateway timeout"

Q850map['111'] = dict()
Q850map['111']['isdn'] = "protocol error"
Q850map['111']['sip'] = "500 Server internal error"


Q850map['127'] = dict()
Q850map['127']['isdn'] = "inter-working unspecified"
Q850map['127']['sip'] = "500 Server internal error"


Q850map['487'] = dict()
Q850map['487']['isdn'] = "ORIGINATOR_CANCEL"
Q850map['487']['sip'] = "487 Request Terminated"

Q850map['500'] = dict()
Q850map['500']['isdn'] = "CRASH"
Q850map['500']['sip'] = ""

Q850map['501'] = dict()
Q850map['501']['isdn'] = "SYSTEM_SHUTDOWN"
Q850map['501']['sip'] = ""

Q850map['502'] = dict()
Q850map['502']['isdn'] = "LOSE_RACE"
Q850map['502']['sip'] = ""

Q850map['503'] = dict()
Q850map['503']['isdn'] = "MANAGER_REQUEST"
Q850map['503']['sip'] = ""

Q850map['600'] = dict()
Q850map['600']['isdn'] = "BLIND_TRANSFER"
Q850map['600']['sip'] = ""

Q850map['601'] = dict()
Q850map['601']['isdn'] = "ATTENDED_TRANSFER"
Q850map['601']['sip'] = ""


Q850map['602'] = dict()
Q850map['602']['isdn'] = "ALLOTTED_TIMEOUT"
Q850map['602']['sip'] = ""


Q850map['603'] = dict()
Q850map['603']['isdn'] = "USER_CHALLENGE"
Q850map['603']['sip'] = ""

Q850map['604'] = dict()
Q850map['604']['isdn'] = "MEDIA_TIMEOUT"
Q850map['604']['sip'] = ""

Q850map['605'] = dict()
Q850map['605']['isdn'] = "PICKED_OFF"
Q850map['605']['sip'] = ""


Q850map['606'] = dict()
Q850map['606']['isdn'] = "USER_NOT_REGISTERED"
Q850map['606']['sip'] = ""


Q850map['607'] = dict()
Q850map['607']['isdn'] = "PROGRESS_TIMEOUT"
Q850map['607']['sip'] = ""

Q850map['609'] = dict()
Q850map['609']['isdn'] = "GATEWAY_DOWN"
Q850map['609']['sip'] = ""

#ike notify error type
ikenotifyerror = [
"UNSUPPORTED_CRITICAL_PAYLOAD",
"INVALID_IKE_SPI",
"INVALID_MAJOR_VERSION",
"INVALID_SYNTAX",
"INVALID_MESSAGE_ID",
"INVALID_SPI",
"NO_PROPOSAL_CHOSEN",
"INVALID_KE_PAYLOAD",
"AUTHENTICATION_FAILED",
"SINGLE_PAIR_REQUIRED",
"NO_ADDITIONAL_SAS",
"INTERNAL_ADDRESS_FAILURE",
"FAILED_CP_REQUIRED",
"TS_UNACCEPTABLE",
"INVALID_SELECTORS",
"UNACCEPTABLE_ADDRESSES",
"TEMPORARY_FAILURE",
"CHILD_SA_NOT_FOUND",
#"INITIAL_CONTACT",
#"SET_WINDOW_SIZE",
#"ADDITIONAL_TS_POSSIBLE",
#"IPCOMP_SUPPORTED",
#"NAT_DETECTION_SOURCE_IP",
#"NAT_DETECTION_DESTINATION_IP",
#"COOKIE",
#"USE_TRANSPORT_MODE",
#"HTTP_CERT_LOOKUP_SUPPORTED",
#"REKEY_SA",
#"ESP_TFC_PADDING_NOT_SUPPORTED",
#"NON_FIRST_FRAGMENTS_ALSO",
#"MOBIKE_SUPPORT",
#"NO_ADDITIONAL_ADDRESSES",
#"UPDATE_SA_ADDRESSES",
#"COOKIE2",
#"AUTH_LIFETIME",
#"MULTIPLE_AUTH_SUPPORTED",
#"EAP_ONLY_AUTHENTICATION"
]

mypayloadtype = [
    "Security Assocoation (33)",
    "Key Exchange (34)",
    "Traffic Selector - Initiator (44)",
    "Traffic Selector - Responder (45)",
    "Extensible Authentication (48)",
    "Encrypted and Authenticated (46)",
    "Authentication (39)",
    "Notify (41)",
    "Nonce (40)",
    "Nonce",
    "Configuration",
    "Delete (42)"
]


#bug 580143, MT_Call_Deattach can be a good example

from eventhandler import *

module_UE="UE"
module_ImsCM="ImsCM"
module_Phone="Phone"
module_Service="Service"
module_Security="Security"
#module_Lemon="Sip Stack"
module_CP="CP"
module_dialer="Dialer"

class eventType():
    SEPERATOR = 1 #seperator line
    SELFREF = 2   #self reference edge
    EDGE = 3      # normal edge


class eventArray():
    def __init__(self):
        self.array = list()

    def addEvent(self, key, module, eventType = eventType.SEPERATOR, eventHandler = matchone, color= "black", groupnum=1):
        event = dict()
        event['key'] = key
        event['module'] = module
        event['eventType'] = eventType
        event['eventHandler'] = eventHandler
        event['color'] = color
        event['groupnum'] = groupnum
        self.array.append(event)

    def getarray(self):
        return self.array

dialerEvent = eventArray()
imscmEvent = eventArray()
phoneEvent = eventArray()
securityEvent = eventArray()
serviceEvent = eventArray()

processmap = dict()
processmap['com.sprd.ImsConnectionManager'] = imscmEvent.getarray()
processmap['com.android.phone'] = phoneEvent.getarray()
processmap['com.android.dialer'] = dialerEvent.getarray()
processmap['com.sprd.vowifi.security'] = securityEvent.getarray()
processmap['com.spreadtrum.vowifi'] = serviceEvent.getarray()


#dialer part
### hold
#FIXME: later should add more phrase to indicate



dialerEvent.addEvent("(Putting the call on hold)", module_dialer, eventType = eventType.EDGE)

### resume
dialerEvent.addEvent("(Removing the call from hold)", module_dialer, eventType = eventType.EDGE)
dialerEvent.addEvent("(Swapping call to foreground)", module_dialer, eventType = eventType.EDGE)
#------------------------------------------------------------------------------------
#ImsCM part
##ImsConnectionManagerMonitor
###start up wfc status
#imscmEvent.addEvent("(Wifi-calling is.*)", module_ImsCM)
###bind service
imscmEvent.addEvent("(\[bind.*)", module_ImsCM, eventType = eventType.EDGE)
##Utils
###switch to wifi
imscmEvent.addEvent("\[(Switch to Vowifi)\]", module_ImsCM, eventType = eventType.EDGE, color = "blue")
###switch to volte
imscmEvent.addEvent("\[(Switch to Volte)\]", module_ImsCM, eventType = eventType.EDGE, color = "blue")
###Handover to Vowifi
imscmEvent.addEvent("\[(Handover to Vowifi)\]", module_ImsCM, eventType = eventType.EDGE, color = "blue")
###Handover to Volte
imscmEvent.addEvent("\[(Handover to Volte)\]", module_ImsCM,  eventType = eventType.EDGE, color = "blue")
###Release Vowifi resource
imscmEvent.addEvent("\[(Release Vowifi resource)\]", module_ImsCM, eventType = eventType.EDGE)
###Set Vowifi unavailable
imscmEvent.addEvent("\[(Set Vowifi unavailable)\]", module_ImsCM, eventType = eventType.EDGE, color = "red")
###[Cancel current request]
imscmEvent.addEvent("\[(Cancel current request)\]", module_ImsCM)
###[hung up Vowifi call]
imscmEvent.addEvent("\[(hung up Vowifi call)\]", module_ImsCM, eventType=eventType.EDGE, color = "blue")
###[popup Vowifi unavailable notification]
imscmEvent.addEvent("\[(popup Vowifi unavailable notification)\]", module_ImsCM, eventType=eventType.SELFREF)

##TODO:ImsConnectionManagerRelianceService
#------------------------------------------------------------------------------------
##ImsConnectionManagerService
###release vowifi resource
imscmEvent.addEvent("(releaseVoWifiResource:.*)", module_ImsCM)
###vowifi unavailable
imscmEvent.addEvent("(vowifiUnavailable:.*)", module_ImsCM)
###cancel request
imscmEvent.addEvent("(cancelCurrentRequest:.*)", module_ImsCM)
###switchOrHandoverVowifi:
imscmEvent.addEvent("(switchOrHandoverVowifi:.*)", module_ImsCM)
###handoverToVolte
imscmEvent.addEvent("(handoverToVolte:.*)", module_ImsCM)
###hungUpVowifiCall
imscmEvent.addEvent("(hungUpVowifiCall:.*)", module_ImsCM)
###operation success
imscmEvent.addEvent("(operationSuccessed:.*)", module_ImsCM)
###operation failed
imscmEvent.addEvent("(operationFailed:.*)", module_ImsCM)
###imsCallEnd
imscmEvent.addEvent("(imsCallEnd:.*)", module_ImsCM)

###CP module
imscmEvent.addEvent("ImsConnectionManagerService:(.*CP module.*)", module_ImsCM)
###onNoRtpReceived
imscmEvent.addEvent("(onNoRtpReceived:.*)", module_ImsCM)
###onRtpReceived
imscmEvent.addEvent("(onRtpReceived:.*)", module_ImsCM)
###onProcessDpdDisconnectedError
imscmEvent.addEvent("(onProcessDpdDisconnectedError.*)", module_ImsCM)
###onProcessSipTimeoutError
imscmEvent.addEvent("(onProcessSipTimeoutError:.*)", module_ImsCM)
###onProcessUnsolicitedSipLogoutError
imscmEvent.addEvent("(onProcessUnsolicitedSipLogoutError:.*)", module_ImsCM)
###onProcessSecurityRekeyError
imscmEvent.addEvent("(onProcessSecurityRekeyError:.*)", module_ImsCM)
###onProcessUnsolicitedEpdgStopError
imscmEvent.addEvent("(onProcessUnsolicitedEpdgStopError:.*)", module_ImsCM)
###onVoWiFiError
imscmEvent.addEvent("(onVoWiFiError:.*)", module_ImsCM)
###ServiceStateChanged
#seems too verbose
#addEvent("(ServiceStateChanged:.*)", module_ImsCM)
###onCallStateChanged
imscmEvent.addEvent("(onCallStateChanged:.*)", module_ImsCM)

##post-ping
##wifi connected
imscmEvent.addEvent('(wifi is connected)', module_ImsCM, eventType = eventType.EDGE, color="blue")
imscmEvent.addEvent("NetworkUtils: (Local IP address is:.*)", module_ImsCM)


##airplane open
imscmEvent.addEvent('(open airplane mode)', module_ImsCM , eventType = eventType.EDGE, color="blue")
##airplaneclose
imscmEvent.addEvent('(close airplane mode)', module_ImsCM,eventType = eventType.EDGE, color="blue")

##wifi disconnected
imscmEvent.addEvent('(wifi is disconnected)', module_ImsCM, eventType = eventType.EDGE, color="blue")
##wifi calling
imscmEvent.addEvent('database has changed, mIsWifiCallingEnabled = (.*)', module_ImsCM, eventType = eventType.EDGE, eventHandler=wfcstatus)


##no rtp
imscmEvent.addEvent("ImsConnectionManagerService:(.*mNoRtpTimes.*)", module_ImsCM)

## more log about rssi
##D:\code\log\otherlog\stephen\1236_in_voice_call_auto_handover_to_volte


imscmEvent.addEvent("(getPhoneStateListenerEx: Both new Volte and new Vowifi are not registered, releaseAllTimer.*)", module_ImsCM)
imscmEvent.addEvent("(createTimerTask: Wifi or Lte conditions are not satisfied, don't create timer task.*)", module_ImsCM)

#volte threshold
imscmEvent.addEvent("(createTimerTask: create.*threshold timer task during .* idle.*)", module_ImsCM)
imscmEvent.addEvent("(loopProcess.*Threshold: .* maybe switch to.*)", module_ImsCM)
imscmEvent.addEvent("(loopProcess.*Threshold: .* switch to.*)", module_ImsCM)
imscmEvent.addEvent("(loopProcess.*Threshold: .* maybe handover to .*)", module_ImsCM)
imscmEvent.addEvent("(loopProcess.*Threshold: .* handover to .*)", module_ImsCM)
imscmEvent.addEvent("(create.*ThresholdTimerTask Wifi or Lte conditions are not satisfied, release.*)", module_ImsCM)
'''
###wifi threshold
addEvent("(createTimerTask: create \[Idle\] threshold timer task during Vowifi idle.*)", module_ImsCM)
addEvent("(loopProcessIdleThreshold: Vowifi maybe switch to Volte.*)", module_ImsCM)
addEvent("(loopProcessIdleThreshold: Vowifi switch to Volte.*)", module_ImsCM)

### audio volte
addEvent("(createTimerTask: create \[Audio\] threshold timer task during Volte call.*)", module_ImsCM)
addEvent("(loopProcessAudioThreshold: Volte maybe handover to Vowifi.*)", module_ImsCM)
addEvent("(loopProcessAudioThreshold: Volte handover to Vowifi.*)", module_ImsCM)

### video volte
addEvent("(createTimerTask: create \[Video\] threshold timer task during Volte call)", module_ImsCM)
addEvent("(loopProcessVideoThreshold: Volte maybe handover to Vowifi.*)", module_ImsCM)
addEvent("(loopProcessVideoThreshold: Volte handover to Vowifi.*)", module_ImsCM)
### audio vowifi
addEvent("(createTimerTask: create \[Audio\] threshold timer task during Vowifi call)", module_ImsCM)
addEvent("(loopProcessAudioThreshold: Vowifi maybe handover to Volte.*)", module_ImsCM)
addEvent("(loopProcessAudioThreshold: Vowifi handover to Volte.*)", module_ImsCM)

### video vowifi
addEvent("(createTimerTask: create \[Video\] threshold timer task during Vowifi call)", module_ImsCM)
addEvent("(loopProcessVideoThreshold: Vowifi maybe handover to Volte.*)", module_ImsCM)
addEvent("(loopProcessVideoThreshold: Vowifi handover to Volte.*)", module_ImsCM)
'''
###misc
imscmEvent.addEvent("(createQosWifiRssiTimerTask: Wifi rssi isn't better, release.*)", module_ImsCM)
imscmEvent.addEvent("(createQosWifiRssiTimerTask: Conditions are not satisfied, release.*)", module_ImsCM)
### audio/video qos
imscmEvent.addEvent("(loopProcess.*Qos: Vowifi maybe handover to Volte.*)", module_ImsCM)
imscmEvent.addEvent("(loopProcess.*Qos: Vowifi maybe handover to Volte.*)", module_ImsCM)
imscmEvent.addEvent("(loopProcess.*Qos: Vowifi handover to Volte.*)", module_ImsCM)



### sim card
imscmEvent.addEvent("(turn off primary SIM card)", module_ImsCM)

##msg pending
# ImsConnectionManagerService: handleMessageHandoverToVowifi: mIsPendingProcess
#D:\code\log\bug_log\vit_log\2016_10_25\modem_log-0650-vowifiregisterfail-2


#------------------------------------------------------------------------------------

#phone imsservice logre
##vowifi/volte icon
phoneEvent.addEvent("updateImsFeatures->volteEnable:(.*) wifiEnable:(.*)", module_Phone, eventType=eventType.EDGE, eventHandler=geticon,groupnum=2)
##ims reg addr
phoneEvent.addEvent("setIMSRegAddress addr = (.*)", module_Phone, eventType=eventType.EDGE, eventHandler=imsregaddr)
## start vowifi/volte call
phoneEvent.addEvent("createCallSession-> start(.*)", module_Phone, eventType=eventType.EDGE, eventHandler=startcall, color = "blue")

#Adapter Part
##VoWifiSecurityManager

###update data router
##update datarouter
phoneEvent.addEvent('VoWifiCallManager: Update the call state to data router. state: (.*)', module_Phone, eventType = eventType.EDGE, eventHandler=drstatus)
###s2b start
phoneEvent.addEvent("(Start the s2b attach.)",module_Phone, eventType = eventType.EDGE)
###deattach
#phoneEvent.addEvent("(Try to de-attach, is handover:.*)", module_Phone)
###force stop
#phoneEvent.addEvent("(Force stop the s2b.)", module_Phone)
###s2b success
#phoneEvent.addEvent("(S2b attach success.)", module_Phone)
###s2b failed
#phoneEvent.addEvent("(S2b attach failed, errorCode:.*)", module_Phone)
###s2b state change
#phoneEvent.addEvent("(S2b attach progress state changed to.*)", module_Phone)
###s2b stop
#phoneEvent.addEvent("(S2b attach stopped, errorCode: .*)", module_Phone)
#------------------------------------------------------------------------------------
##VoWifiRegisterManager
###prepare login
phoneEvent.addEvent("(Prepare the info before login), subId is:.*", module_Phone, eventType=eventType.EDGE)
###try to login
#phoneEvent.addEvent("(Try to login to the ims, current register state: .*)", module_Phone)
###Login info: ip, p-cscf
phoneEvent.addEvent("Login with the local ip: (.*), pcscf ip: (.*)", module_Phone, eventType=eventType.EDGE, eventHandler=loginstatus, groupnum=2)
###logout
phoneEvent.addEvent("Try to logout from the ims, current register state: (.*)", module_Phone, eventType=eventType.EDGE, eventHandler=logoutstatus)
###Re-register, do this in service
#phoneEvent.addEvent("(Re-register, with the type:.*)", module_Phone)
###force stop, no need to track
#phoneEvent.addEvent("(Stop current register process. registerState:.*)", module_Phone)

### security callback
phoneEvent.addEvent("Get the security callback:(.*)", module_Phone, eventType=eventType.EDGE, eventHandler=s2bstatus)
### register callback
phoneEvent.addEvent("Get the register state changed callback: {\"event_code\":.*,\"event_name\":\"(.*)\",\"state_code\":(.*)}" , module_Phone, eventType=eventType.EDGE, eventHandler=regstatus, groupnum=2)

###call related event
#phoneEvent.addEvent("(Handle the event.*for the call.*)", module_Phone)


###mute
phoneEvent.addEvent("Mutes\((.*)\)the mic for the active call", module_Phone, eventType=eventType.EDGE, eventHandler=mutestatus)
###start call, #important key words
phoneEvent.addEvent("Initiates an ims call with (.*)", module_Phone, eventType=eventType.EDGE, eventHandler=makecallstatus)
###start conf call
phoneEvent.addEvent("(Initiates an ims conference call with.*)", module_Phone)
###accept
phoneEvent.addEvent("(Accept an incoming call with call type is.*)", module_Phone)
###reject
phoneEvent.addEvent("(Reject an incoming call as the reason is.*)", module_Phone)
###terminate
phoneEvent.addEvent("(Terminate a call as the reason is.*)", module_Phone)
###hold
phoneEvent.addEvent("(Hold a call with the media profile:.*)", module_Phone)
###resume
phoneEvent.addEvent("(Continues a call with the media profile.*)", module_Phone)
###merge
phoneEvent.addEvent("(Merge the active & hold call)", module_Phone)
###update
phoneEvent.addEvent("(Update the current call's type to .*)", module_Phone)
###invite conf participants
phoneEvent.addEvent("(Request server to invite participants:.*)", module_Phone)
###remove conf participants
phoneEvent.addEvent("(Remove the participants:.*)", module_Phone)
###send dtmf
phoneEvent.addEvent("(sendDtmf.*)", module_Phone)
###start dtmf
phoneEvent.addEvent("(startDtmf.*)", module_Phone)
###send ussd
phoneEvent.addEvent("(Send an USSD message:.*)", module_Phone)

###start camera
phoneEvent.addEvent("(Try to start the camera:.*)", module_Phone)

###stop camera
phoneEvent.addEvent("(Try to stop the camera for the call:.*)", module_Phone)
###modify request
phoneEvent.addEvent("(Try to send the modify request, isVideo:.*)", module_Phone)

###start local render
phoneEvent.addEvent("(Try to start the local render for the call:.*)", module_Phone)
###stop local render
phoneEvent.addEvent("(Try to stop the local render for the call:.*)", module_Phone)
###start remote render
phoneEvent.addEvent("(Try to start the remote render for the call:.*)", module_Phone)
### stop remote render
phoneEvent.addEvent("(Try to stop the remote render for the call:.*)", module_Phone)
### start capture
phoneEvent.addEvent("(try to start capture for the call:.*)", module_Phone)
### stop capture
phoneEvent.addEvent("(Try to stop capture for the call:.*)", module_Phone)
###start video trans
phoneEvent.addEvent("(Try to start the video transmission for the call:.*)", module_Phone)
### stop video trans
phoneEvent.addEvent("(Try to stop the video transmission for the call:.*)", module_Phone)
###local rotate
phoneEvent.addEvent("(Try to rotate local render for the call:.*)", module_Phone)
### remote rotate
phoneEvent.addEvent("(Try to rotate remote render for the call:.*)", module_Phone)


###set pause image
phoneEvent.addEvent("(Set the pause image to.*)", module_Phone)
###invite conf call
phoneEvent.addEvent("(Try to invite this call.*to the conference call.*)", module_Phone)
#0 VOLTE; 1 VOWIFI; 2 END Call,  value can be string/number
#need to do here
#phoneEvent.addEvent("(Update the call state to data router. state: .*)", module_Phone)
#------------------------------------------------------------------------------------
#Service part
##RegisterService

#aka response
serviceEvent.addEvent("Get the challenge response: TAG = (.*),.*", module_Service, eventType=eventType.EDGE, eventHandler=akastatus)

#re-register
serviceEvent.addEvent("Try to start the re-register process with the type: (.*), info: (.*)", module_Service, eventType=eventType.EDGE, eventHandler=reregstatus, groupnum=2)

#"Try to reset the sip stack."
serviceEvent.addEvent("(Try to reset the sip stack)", module_Service, eventType=eventType.EDGE, color="blue")

#comment here
#serviceEvent.addEvent("(Notify the event:.*)", module_Service)

#reg status code comes here
#only care about the adapter's log
#serviceEvent.addEvent("(RegisterService.*Get the register state changed callback.*)", module_Service)


#------------------------------------------------------------------------------------
#lemon part
##reinvite ack not received
serviceEvent.addEvent("(ACK to reinvite with no offer does not received when call.*)", module_Service)



### MTC_EBASE_S2B , MTC_EBASE_REG

#security part
securityEvent.addEvent("LEMON.*(imsi is.*)", module_Security)
securityEvent.addEvent("SecurityS2bBinder: INFO: (ping.*)", module_Security)

