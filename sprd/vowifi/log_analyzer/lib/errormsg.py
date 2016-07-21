#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

#TODO:
# 1. define different event type: 1. user action 2. msg deliver 3. self fsm 4. error indication


#adapter interact with service, imscm, lemon, security
#imscm interact with adapter, user, cp
#service interact with lemon, adapter


#define role name
element_UE="UE"
element_ImsCM="ImsCM"
element_Phone="Phone_Adapter"
element_Service="Service"
element_Security="Security"
element_Lemon="Sip Stack"
element_CP="CP"
#define action
direct_send='send'
direct_recv='recv'

class errorbase():
    def __init__(self, owner):
        self.errorpattern = ''
        self.keys = list()
        self.diagkeys = list()
        self.owner = owner

    def setepattern(self, epattern):
        self.errorpattern = epattern

    def addkey(self, key):
        self.keys.append(key)

    def addDiagKey(self, key, role, action):
        diagkey = dict()
        diagkey['key'] =  key
        diagkey['role'] = role
        #role's action
        diagkey['action'] = action
        self.diagkeys.append(diagkey)


lemonmsg = errorbase(owner=element_Lemon)
#add mme error log
lemonmsg.setepattern("LEMON.*: ERROR")
lemonmsg.addkey("fsm\(.*\)")
lemonmsg.addkey("\[TIMER.*\]")
lemonmsg.addkey("process request")
lemonmsg.addkey("process response")
lemonmsg.addkey("gui notify")


imscmmsg = errorbase(owner=element_ImsCM)
imscmmsg.setepattern('')


imscmmsg.addkey("database has changed, mIsWifiCallingEnabled")
imscmmsg.addDiagKey("database has changed, mIsWifiCallingEnabled", element_UE, direct_send)
imscmmsg.addkey("wifi is connected")
imscmmsg.addDiagKey("wifi is connected", element_UE, direct_send)
imscmmsg.addkey("wifi is disconnected")
imscmmsg.addDiagKey("wifi is disconnected", element_UE, direct_send)
imscmmsg.addkey("open airplane mode")
imscmmsg.addDiagKey("open airplane mode", element_UE, direct_send)

imscmmsg.addkey("close airplane mode")
imscmmsg.addDiagKey("close airplane mode", element_UE, direct_send)

imscmmsg.addkey("popup Vowifi unavailable notification")
imscmmsg.addDiagKey("popup Vowifi unavailable notification", element_UE, direct_recv)

imscmmsg.addkey("Switch to Vowifi")
imscmmsg.addDiagKey("Switch to Vowifi", element_Phone, direct_recv)

imscmmsg.addkey("Switch to Volte")
imscmmsg.addDiagKey("Switch to Volte", element_Phone, direct_recv)

imscmmsg.addkey("Handover to Vowifi")
imscmmsg.addDiagKey("Handover to Vowifi", element_Phone, direct_recv)


imscmmsg.addkey("Handover to Volte")
imscmmsg.addDiagKey("Handover to Volte", element_Phone, direct_recv)

imscmmsg.addkey("Set Vowifi unavailable")
imscmmsg.addDiagKey("Set Vowifi unavailable", element_Phone, direct_recv)

imscmmsg.addkey("Cancel current request")
imscmmsg.addDiagKey("Cancel current request", element_Phone, direct_recv)

imscmmsg.addkey("hung up Vowifi call")
imscmmsg.addDiagKey("hung up Vowifi call", element_Phone, direct_recv)


imscmmsg.addkey("vowifiUnavailable: don't release vowifi resource")
imscmmsg.addDiagKey("vowifiUnavailable: don't release vowifi resource", element_Phone, direct_recv)

imscmmsg.addkey("vowifiUnavailable: release vowifi resource at first")
imscmmsg.addDiagKey("vowifiUnavailable: release vowifi resource at first", element_Phone, direct_recv)

imscmmsg.addkey("\[Release Vowifi resource\]")
imscmmsg.addDiagKey("\[Release Vowifi resource\]", element_Phone, direct_recv)

imscmmsg.addkey("switchOrHandoverVowifi")
imscmmsg.addDiagKey("switchOrHandoverVowifi", element_Phone, direct_recv)

imscmmsg.addkey("operationSuccessed")
imscmmsg.addDiagKey("operationSuccessed", element_Phone,direct_send)

imscmmsg.addkey("operationFailed")
imscmmsg.addDiagKey("operationFailed", element_Phone, direct_send)

imscmmsg.addkey("imsCallEnd")

imscmmsg.addkey("onDPDDisconnected")

imscmmsg.addkey("onNoRtpReceived")
imscmmsg.addDiagKey("onNoRtpReceived", element_Phone, direct_send)

imscmmsg.addkey("onProcessSecurityRekeyError")
imscmmsg.addDiagKey("onProcessSecurityRekeyError", element_Phone, direct_send)
imscmmsg.addkey("onProcessUnsolicitedEpdgStopError")
imscmmsg.addDiagKey("onProcessUnsolicitedEpdgStopError", element_Phone, direct_send)

imscmmsg.addkey("CP module un-successfully active PDN, mCallingMode")
imscmmsg.addDiagKey("CP module un-successfully active PDN, mCallingMode", element_Phone, direct_send)
imscmmsg.addkey("CP module successfully active PDN, mCallingMode")

imscmmsg.addDiagKey("CP module successfully active PDN, mCallingMode", element_Phone, direct_send)

imscmmsg.addkey("ImsConnectionManagerService.*mNoRtpTimes")
#FIXME, logic need to refactor
#imscmmsg.addDiagKey("ImsConnectionManagerService.*mNoRtpTimes", )
#imscmmsg.addkey("set rtp no data monitor timer")

#imscmmsg.addkey("vowifiUnavailable: mNoRtpTimes")


#PhoneStateListener
#imscmmsg.addkey("Vowifi is registered")

#imscmmsg.addkey("Volte is registered")

adaptermsg = errorbase(owner=element_Phone)

#warning/error
adaptermsg.setepattern(" [W|E] \[Adapter\]")

#s2b
adaptermsg.addkey("Start the s2b attach")
adaptermsg.addDiagKey("Start the s2b attach", element_Security, direct_recv)
adaptermsg.addkey("Try to de-attach")
adaptermsg.addDiagKey("Try to de-attach", element_Security, direct_recv)
adaptermsg.addkey("Force stop the s2b")
adaptermsg.addDiagKey("Force stop the s2b", element_Security, direct_recv)

adaptermsg.addkey("S2b attach success")

adaptermsg.addDiagKey("S2b attach success", element_Security, direct_send)

adaptermsg.addkey("S2b attach failed")
adaptermsg.addDiagKey("S2b attach failed", element_Security, direct_send)

adaptermsg.addkey("S2b attach progress state changed to")
adaptermsg.addDiagKey("S2b attach progress state changed to", element_Security, direct_send)

adaptermsg.addkey("S2b attach stopped")
adaptermsg.addDiagKey("S2b attach stopped", element_Security, direct_send)


#reg
adaptermsg.addkey("VoWifiRegisterManager: IMPI is")
adaptermsg.addkey("VoWifiRegisterManager: IMPU array length is")
adaptermsg.addkey("RegisterService: Update the SIM account settings")

#call related
adaptermsg.addkey("Initiates an ims call with")
adaptermsg.addDiagKey("Initiates an ims call with", element_Service,direct_recv)
adaptermsg.addkey("Initiates an ims conference call with")
adaptermsg.addDiagKey("Initiates an ims conference call with", element_Service, direct_recv)
adaptermsg.addkey("Start the conference with phone numbers")

adaptermsg.addkey("Reject an incoming call as the reason is")
adaptermsg.addDiagKey("Reject an incoming call as the reason is", element_Service, direct_recv)

adaptermsg.addkey("Accept an incoming call with call type is")
adaptermsg.addDiagKey("Accept an incoming call with call type is", element_Service, direct_recv)

adaptermsg.addkey("Terminate a call as the reason is")
adaptermsg.addDiagKey("Terminate a call as the reason is", element_Service, direct_recv)
adaptermsg.addkey("Hold a call with the media profile")
adaptermsg.addDiagKey("Hold a call with the media profile", element_Service, direct_recv)

adaptermsg.addkey("Continues a call with the media profile")
adaptermsg.addDiagKey("Continues a call with the media profile", element_Service ,direct_recv)

adaptermsg.addkey("Merge the active & hold call")
adaptermsg.addDiagKey("Merge the active & hold call", element_Service, direct_recv)

adaptermsg.addkey("Update the current call's type to")
adaptermsg.addDiagKey("Update the current call's type to", element_Service, direct_recv)

adaptermsg.addkey("Extends this call to conference call")
adaptermsg.addDiagKey("Extends this call to conference call", element_Service ,direct_recv)

adaptermsg.addkey("Remove the participants")
adaptermsg.addDiagKey("Remove the participants", element_Service, direct_recv)

adaptermsg.addkey("Request server to invite participants")
adaptermsg.addDiagKey("Request server to invite participants", element_Service, direct_recv)


adaptermsg.addkey("sendDtmf")
adaptermsg.addDiagKey("sendDtmf", element_Service, direct_recv)

adaptermsg.addkey("startDtmf")
adaptermsg.addDiagKey("startDtmf", element_Service, direct_recv)

adaptermsg.addkey("Try to start the camera")
adaptermsg.addDiagKey("Try to start the camera", element_Service, direct_recv)

adaptermsg.addkey("Try to stop the camera for the call")
adaptermsg.addDiagKey("Try to stop the camera for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to start the local render for the call")
adaptermsg.addDiagKey("Try to start the local render for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to stop the local render for the call")
adaptermsg.addDiagKey("Try to stop the local render for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to start capture for the call")
adaptermsg.addDiagKey("Try to start capture for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to start the video transmission for the call")
adaptermsg.addDiagKey("Try to start the video transmission for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to stop the video transmission for the call")
adaptermsg.addDiagKey("Try to stop the video transmission for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to rotate local render for the call")
adaptermsg.addDiagKey("Try to rotate local render for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to rotate remote render for the call")
adaptermsg.addDiagKey("Try to rotate remote render for the call", element_Service, direct_recv)

adaptermsg.addkey("Try to send the modify request, isVideo")
adaptermsg.addDiagKey("Try to send the modify request, isVideo", element_Service, direct_recv)

adaptermsg.addkey("Try to query the call barring with the type")
adaptermsg.addDiagKey("Try to query the call barring with the type", element_Service, direct_recv)

adaptermsg.addkey("Handle the rotate message, the device orientation")
adaptermsg.addDiagKey("Handle the rotate message, the device orientation", element_UE, direct_send)

adaptermsg.addkey("VoWifiRegisterManager: Get the register state changed callback")
adaptermsg.addDiagKey("VoWifiRegisterManager: Get the register state changed callback" , element_Service, direct_send)

adaptermsg.addkey("The current orientation is 90 or 270")

adaptermsg.addkey("Get the new angle")

adaptermsg.addkey("Try to terminate all the calls with wifi state:")

adaptermsg.addkey("Update the incoming call action to")

adaptermsg.addkey("Update the call state to data router. state")

adaptermsg.addkey("Try to get the packet lose")

adaptermsg.addkey("Try to get the jitter")

adaptermsg.addkey("Add the call")

adaptermsg.addkey("Remove the call")


adaptermsg.addkey("Handle the alerted or outgoing call")

adaptermsg.addkey("Handle the incoming call")

adaptermsg.addkey("Handle the termed call")
adaptermsg.addkey("Handle the talking call")
adaptermsg.addkey("Handle the hold or resume event")
adaptermsg.addkey("Handle the call update ok")
adaptermsg.addkey("Handle the call add video request")
adaptermsg.addkey("Handle the call is focus")
adaptermsg.addkey("Handle video resize")
adaptermsg.addkey("Handle the conference alerted")
adaptermsg.addkey("will be invite to this conference call")
adaptermsg.addkey("Notify the merge complete")
adaptermsg.addkey("Handle the conference disconnected")
adaptermsg.addkey("Handle the conference participant update result")
adaptermsg.addkey("Get the invite accept result for the user")
adaptermsg.addkey("Get the invite failed result for the user")
adaptermsg.addkey("Handle the call do not received the rtp in 5s")

servicemsg = errorbase(owner=element_Service)


servicemsg.setepattern(" [E|W] \[VoWifiService\]")
servicemsg.addkey("RegisterService: Get the register state changed callback")
servicemsg.addDiagKey("RegisterService: Get the register state changed callback", element_Lemon, direct_send)

servicemsg.addkey("Establishing call with video or audio")
servicemsg.addDiagKey("Establishing call with video or audio", element_Lemon, direct_recv)

servicemsg.addkey("Establish the session call")
servicemsg.addDiagKey("Establish the session call", element_Lemon, direct_recv)

servicemsg.addkey("Set the call.*mute as")
servicemsg.addDiagKey("Set the call.*mute as", element_Lemon, direct_recv)

#ImsReasonInfo.java

servicemsg.addkey("Terminate the call, sessionId")
servicemsg.addDiagKey("Terminate the call, sessionId", element_Lemon, direct_recv)

servicemsg.addkey("Hold the call, sessionId")
servicemsg.addDiagKey("Hold the call, sessionId", element_Lemon, direct_recv)

servicemsg.addkey("Resume the call, sessionId")
servicemsg.addDiagKey("Resume the call, sessionId", element_Lemon, direct_recv)

servicemsg.addkey("Send the DTMF info, sessionId")
servicemsg.addDiagKey("Send the DTMF info, sessionId", element_Lemon, direct_recv)

servicemsg.addkey("Answer the call, sessionId")
servicemsg.addDiagKey("Answer the call, sessionId", element_Lemon, direct_recv)

servicemsg.addkey("Update the call, sessionId")
servicemsg.addDiagKey("Update the call, sessionId", element_Lemon, direct_recv)


servicemsg.addkey("Response a update request for the call, sessionId")
servicemsg.addDiagKey("Response a update request for the call, sessionId", element_Lemon, direct_recv)

servicemsg.addkey("Try to start the conference call with the phone numbers")
servicemsg.addDiagKey("Try to start the conference call with the phone numbers", element_Lemon, direct_recv)

servicemsg.addkey("Try to init the conference resource native. is video")
servicemsg.addDiagKey("Try to init the conference resource native. is video", element_Lemon, direct_recv)

servicemsg.addkey("Try to setup the conference call")
servicemsg.addDiagKey("Try to setup the conference call", element_Lemon, direct_recv)

servicemsg.addkey("Hold the conference call, confId")
servicemsg.addDiagKey("Hold the conference call, confId", element_Lemon, direct_recv)

servicemsg.addkey("Resume the conference call, confId")
servicemsg.addDiagKey("Resume the conference call, confId", element_Lemon, direct_recv)

servicemsg.addkey("Add the members for the conference")
servicemsg.addDiagKey("Add the members for the conference", element_Lemon, direct_recv)

servicemsg.addkey("The new added members")
servicemsg.addDiagKey("The new added members", element_Lemon, direct_recv)

servicemsg.addkey("Accept the conference invite. conference id")
servicemsg.addDiagKey("Accept the conference invite. conference id", element_Lemon, direct_recv)

servicemsg.addkey("Terminate the conference call, confId")
servicemsg.addDiagKey("Terminate the conference call, confId", element_Lemon, direct_recv)

servicemsg.addkey("Kick off members from the conference call")
servicemsg.addDiagKey("Kick off members from the conference call", element_Lemon, direct_recv)

servicemsg.addkey("Set the conference call.*mute as")
servicemsg.addDiagKey("Set the conference call.*mute as", element_Lemon, direct_recv)

servicemsg.addkey("Set the camera capabilities, width")


servicemsg.addkey("VoWifiSerService: Try to start the audio stream")

#servicemsg.addkey("VoWifiSerService: The call is outgoing")
servicemsg.addkey("VoWifiSerService: Notify the event")
servicemsg.addDiagKey("VoWifiSerService: Notify the event", element_Lemon, direct_send)

servicemsg.addkey("VoWifiSerService: Handle the ZMF notification")
servicemsg.addDiagKey("VoWifiSerService: Handle the ZMF notification", element_Lemon, direct_send)

servicemsg.addkey("The RTP connectivity status is changed")


#rtp, rtcp info
servicemsg.addkey("The call's RTCP info given")
servicemsg.addkey("The call's video capture framerate info given")



servicemsg.addkey("Start the audio for input and output")
servicemsg.addkey("Stop the audio for input and output")

s2bmsg = errorbase(owner=element_Security)
s2bmsg.setepattern('')
s2bmsg.addkey("LEMON.*notifyCallbacks")

#report callback result
s2bmsg.addDiagKey("LEMON.*notifyCallbacks", element_Security, direct_send)

#add pre-ping, post-ping logic
s2bmsg.addkey("LEMON.*ping.*result")
s2bmsg.addkey("SECURITY IKE_KEY")
