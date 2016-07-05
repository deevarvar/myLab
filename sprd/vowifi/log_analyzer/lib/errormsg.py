#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

#TODO:
# 1. define different event type: 1. user action 2. msg deliver 3. self fsm 4. error indication


#adapter interact with service, imscm, lemon, security
#imscm interact with adapter, user, cp
#service interact with lemon, adapter

class errorbase():
    def __init__(self):
        self.errorpattern = ''
        self.keys = list()

    def setepattern(self, epattern):
        self.errorpattern = epattern

    def addkey(self, key):
        self.keys.append(key)

lemonmsg = errorbase()
lemonmsg.setepattern("LEMON.*: ERROR")
lemonmsg.addkey("fsm\(.*\)")
lemonmsg.addkey("\[TIMER.*\]")
lemonmsg.addkey("process request")
lemonmsg.addkey("process respons")
lemonmsg.addkey("gui notify")


imscmmsg = errorbase()
imscmmsg.setepattern('')


imscmmsg.addkey("database has changed, mIsWfcEnabled")
imscmmsg.addkey("wifi is connected")
imscmmsg.addkey("wifi is disconnected")
imscmmsg.addkey("open airplane mode")
imscmmsg.addkey("close airplane mode")

imscmmsg.addkey("Switch to Vowifi")

imscmmsg.addkey("Switch to Volte")
imscmmsg.addkey("Handover to Vowifi")
imscmmsg.addkey("Handover to Volte")
imscmmsg.addkey("Set Vowifi unavailable")
imscmmsg.addkey("Cancel current request")
imscmmsg.addkey("hung up Vowifi call")
imscmmsg.addkey("popup Vowifi unavailable notification")
imscmmsg.addkey("vowifiUnavailable:")
imscmmsg.addkey("cancelCurrentRequest")
imscmmsg.addkey("switchOrHandoverVowifi")
imscmmsg.addkey("operationSuccessed")
imscmmsg.addkey("operationFailed")
imscmmsg.addkey("imsCallEnd")
imscmmsg.addkey("onDPDDisconnected")
imscmmsg.addkey("onNoRtpReceived")
imscmmsg.addkey("CP module")
imscmmsg.addkey("Vowifi is registered")
imscmmsg.addkey("Volte is registered")





adaptermsg = errorbase()

#warning/error
adaptermsg.setepattern(" [W|E] \[Adapter\]")

#s2b
adaptermsg.addkey("Start the s2b attach")
adaptermsg.addkey("S2b attach success")
adaptermsg.addkey("S2b attach failed")
adaptermsg.addkey("S2b attach progress state changed to")
adaptermsg.addkey("Try to de-attach")
adaptermsg.addkey("Force stop the s2b")
#reg
adaptermsg.addkey("VoWifiRegisterManager: IMPI is")
adaptermsg.addkey("VoWifiRegisterManager: IMPU array length is")
adaptermsg.addkey("RegisterService: Update the SIM account settings")

#call related
adaptermsg.addkey("Initiates an ims call with")
adaptermsg.addkey("Initiates an ims conference call with")
adaptermsg.addkey("Start the conference with phone numbers")
adaptermsg.addkey("Reject an incoming call as the reason is")
adaptermsg.addkey("Accept an incoming call with call type is")
adaptermsg.addkey("Terminate a call as the reason is")
adaptermsg.addkey("Hold a call with the media profile")
adaptermsg.addkey("Continues a call with the media profile")
adaptermsg.addkey("Merge the active & hold call")
adaptermsg.addkey("Update the current call's type to")
adaptermsg.addkey("Extends this call to conference call")
adaptermsg.addkey("Remove the participants")
adaptermsg.addkey("Request server to invite participants")
adaptermsg.addkey("sendDtmf")
adaptermsg.addkey("startDtmf")
adaptermsg.addkey("Try to start the camera")
adaptermsg.addkey("Try to stop the camera for the call")
adaptermsg.addkey("Try to start the local render for the call")
adaptermsg.addkey("Try to stop the local render for the call")
adaptermsg.addkey("Try to start capture for the call")
adaptermsg.addkey("Try to start the video transmission for the call")
adaptermsg.addkey("Try to stop the video transmission for the call")
adaptermsg.addkey("Try to rotate local render for the call")
adaptermsg.addkey("Try to rotate remote render for the call")
adaptermsg.addkey("Try to send the modify request, isVideo")
adaptermsg.addkey("Try to query the call barring with the type")
adaptermsg.addkey("Handle the rotate message, the device orientation")
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

servicemsg = errorbase()


servicemsg.setepattern(" [E|W] \[VoWifiService\]")
servicemsg.addkey("RegisterService: Get the register state changed callback")
servicemsg.addkey("Establishing call with video or audio")
servicemsg.addkey("VoWifiSerService: Establish the session call")
servicemsg.addkey("VoWifiSerService: Try to start the audio stream")
#servicemsg.addkey("VoWifiSerService: The call is outgoing")
servicemsg.addkey("VoWifiSerService: Notify the event")
servicemsg.addkey("VoWifiSerService: Handle the ZMF notification")
servicemsg.addkey("The RTP connectivity status is changed")

#rtp, rtcp info
servicemsg.addkey("The call's RTCP info given")
servicemsg.addkey("The call's video capture framerate info given")

#ImsReasonInfo.java
servicemsg.addkey("VoWifiSerService: Terminate the call")

servicemsg.addkey("Start the audio for input and output")
servicemsg.addkey("Stop the audio for input and output")

s2bmsg = errorbase()
s2bmsg.setepattern('')
s2bmsg.addkey("LEMON.*notifyCallbacks")
s2bmsg.addkey("LEMON.*ping.*result")
s2bmsg.addkey("SECURITY IKE_KEY")
