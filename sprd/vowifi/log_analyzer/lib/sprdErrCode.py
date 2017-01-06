#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
# error code mapping for service and IKE
#log pattern:   code: 576|errorCode: 537
#definition:    mtc_cli.h, mtc_s2b.h

#defined in vowifisecuritymanager.java
#security_json_action_s2b_successed, security_json_action_s2b_failed, security_json_action_s2b_stopped
#D:\code\log\india_2016_8_24\bugs\592271\No_Volte_Icon_Idle

Constantregerrcode = dict()
MTC_CLI_REG_BASE=0xE100 #57600

Constantregerrcode[str(int(MTC_CLI_REG_BASE+1))] = "Local request error"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+2))] = "Send message error"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+3))] = "Authentication failed"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+4))] = "Invalid user"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+5))] = "Register timeout"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+6))] = "Register server busy"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+7))] = "Register server not reache"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+8))] = "Register forbidden"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+9))] = "Register unavailable"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+10))] = "Register dns query error"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+11))] = "Register network error"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+12))] = "Register deactived"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+13))] = "Register probation"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+14))] = "Register internal error"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+15))] = "Register no resource"
Constantregerrcode[str(int(MTC_CLI_REG_BASE+16))] = "Other register error"

Constants2berrcode = dict()
MTC_S2B_BASE=0xD200 #53760
Constants2berrcode[str(int(MTC_S2B_BASE))] = "no error"
Constants2berrcode[str(int(MTC_S2B_BASE+1))] = "idle error"
Constants2berrcode[str(int(MTC_S2B_BASE+2))] = "fqdn error"
Constants2berrcode[str(int(MTC_S2B_BASE+3))] = "sainit error"
Constants2berrcode[str(int(MTC_S2B_BASE+4))] = "auth error"
Constants2berrcode[str(int(MTC_S2B_BASE+5))] = "eap error"
Constants2berrcode[str(int(MTC_S2B_BASE+6))] = "auth finish error"
Constants2berrcode[str(int(MTC_S2B_BASE+7))] = "auth resend error"
Constants2berrcode[str(int(MTC_S2B_BASE+8))] = "enter aka error"
Constants2berrcode[str(int(MTC_S2B_BASE+9))] = "resend timeout error"
Constants2berrcode[str(int(MTC_S2B_BASE+10))] = "ipsec rekey error"
Constants2berrcode[str(int(MTC_S2B_BASE+11))] = "IKE rekey error"
Constants2berrcode[str(int(MTC_S2B_BASE+12))] = "IKE reauth error"
Constants2berrcode[str(int(MTC_S2B_BASE+13))] = "IKE termining error"
Constants2berrcode[str(int(MTC_S2B_BASE+14))] = "IKE mobike error"
Constants2berrcode[str(int(MTC_S2B_BASE+15))] = "IKE dpd error"
Constants2berrcode[str(int(MTC_S2B_BASE+198))] = "IKE interrupt stop"
Constants2berrcode[str(int(MTC_S2B_BASE+199))] = "IKE handover stop"
Constants2berrcode[str(int(MTC_S2B_BASE+200))] = "IKE other error"


#some alert definition in  MtcCallConstants.java
#Note, do not enumate every error code here
#because seems service will do the convertion and we only care about the code which is not converted.
Constantcallcode = dict()
MTC_CALL_BASE = 0xE200
Constantcallcode[str(int(MTC_CALL_BASE+41))] = "180 Ringing"
Constantcallcode[str(int(MTC_CALL_BASE+42))] = "182 Queued"
Constantcallcode[str(int(MTC_CALL_BASE+43))] = "183 Progressed"

#Imsreasoninfo.java definition
#just follow getImsReasonInfoCode's logic, not full definition
Constantimsreason = dict()
CODE_UNSPECIFIED = 0
CODE_USER_TERMINATED_BY_REMOTE = 510
CODE_SIP_REQUEST_TIMEOUT = 335
CODE_SIP_BUSY = 338
CODE_SIP_USER_REJECTED = 361
CODE_SIP_REDIRECTED = 321

CODE_USER_TERMINATED = 501
CODE_USER_NOANSWER = 502
CODE_USER_IGNORE = 503
CODE_USER_DECLINE = 504
CODE_LOW_BATTERY = 505
CODE_BLACKLISTED_CALL_ID = 506

Constantimsreason[str(CODE_UNSPECIFIED)] = "Unspecified Code"
Constantimsreason[str(CODE_USER_TERMINATED_BY_REMOTE)] = "Termed by Remote"
Constantimsreason[str(CODE_SIP_REQUEST_TIMEOUT)] = "Request Timeout"
Constantimsreason[str(CODE_SIP_BUSY)] = "User Busy"
Constantimsreason[str(CODE_SIP_USER_REJECTED)] = "User Reject"
Constantimsreason[str(CODE_SIP_REDIRECTED)] = "Request Redirected"

Constantimsreason[str(CODE_USER_TERMINATED)] = "User Terminated"
Constantimsreason[str(CODE_USER_NOANSWER)] = "User No Answer"
Constantimsreason[str(CODE_USER_IGNORE)] = "User Ignore"
Constantimsreason[str(CODE_USER_DECLINE)] = "User Decline"
Constantimsreason[str(CODE_LOW_BATTERY)] = "Low Battery"
Constantimsreason[str(CODE_BLACKLISTED_CALL_ID)] = "Blacklisted callid"

#some definition in EN_MTC_ACC_NET_TYPE
Constantaccnettype = dict()
EN_MTC_ACC_NET_IEEE_802_11 = 1
EN_MTC_ACC_NET_3GPP_E_UTRAN_FDD = 9
Constantaccnettype[str(EN_MTC_ACC_NET_IEEE_802_11)] = "IEEE-802.11"
Constantaccnettype[str(EN_MTC_ACC_NET_3GPP_E_UTRAN_FDD)] = "3GPP-E-UTRAN-FDD"

#adapter definition in RegisterState
Constantregstate = dict()
STATE_IDLE = 0
STATE_PROGRESSING = 1
STATE_CONNECTED = 2
Constantregstate[str(STATE_IDLE)] = "Unreged"
Constantregstate[str(STATE_PROGRESSING)] = "Reging"
Constantregstate[str(STATE_CONNECTED)] = "Reged"


#call type defined in ImsCallProfile.java
Constantcalltype = dict()
CALL_TYPE_VOICE = 2
CALL_TYPE_VT = 4
Constantcalltype[str(CALL_TYPE_VOICE)] = "Voice Call"
Constantcalltype[str(CALL_TYPE_VT)] = "Video Call"

#media profiel defined in ImsStreamMediaProfile.java
#Media Direction
DIRECTION_INVALID = -1
DIRECTION_INACTIVE = 0
DIRECTION_RECEIVE = 1
DIRECTION_SEND = 2
DIRECTION_SEND_RECEIVE = 3
Constantdirection = dict()
Constantdirection[str(DIRECTION_INVALID)] = "invalid"
Constantdirection[str(DIRECTION_INACTIVE)] = "inactive"
Constantdirection[str(DIRECTION_RECEIVE)] = "receiveonly"
Constantdirection[str(DIRECTION_SEND)] = "sendonly"
Constantdirection[str(DIRECTION_SEND_RECEIVE)] = "sendrecv"

#audio info
AUDIO_QUALITY_NONE = 0
AUDIO_QUALITY_AMR = 1
AUDIO_QUALITY_AMR_WB = 2
AUDIO_QUALITY_QCELP13K = 3
AUDIO_QUALITY_EVRC = 4
AUDIO_QUALITY_EVRC_B = 5
AUDIO_QUALITY_EVRC_WB = 6
AUDIO_QUALITY_EVRC_NW = 7
AUDIO_QUALITY_GSM_EFR = 8
AUDIO_QUALITY_GSM_FR = 9
AUDIO_QUALITY_GSM_HR = 10
AUDIO_QUALITY_G711U = 11
AUDIO_QUALITY_G723 = 12
AUDIO_QUALITY_G711A = 13
AUDIO_QUALITY_G722 = 14
AUDIO_QUALITY_G711AB = 15
AUDIO_QUALITY_G729 = 16
AUDIO_QUALITY_EVS_NB = 17
AUDIO_QUALITY_EVS_WB = 18
AUDIO_QUALITY_EVS_SWB = 19
AUDIO_QUALITY_EVS_FB = 20
ConstantAudioQ = dict()
ConstantAudioQ[str(AUDIO_QUALITY_NONE)] = "None Audio"
ConstantAudioQ[str(AUDIO_QUALITY_AMR)] = "AMR"
ConstantAudioQ[str(AUDIO_QUALITY_AMR_WB)] = "AMR WB"
ConstantAudioQ[str(AUDIO_QUALITY_QCELP13K)] = "QCELP13K"
ConstantAudioQ[str(AUDIO_QUALITY_EVRC)] = "EVRC"
ConstantAudioQ[str(AUDIO_QUALITY_EVRC_B)] = "EVRC_B"
ConstantAudioQ[str(AUDIO_QUALITY_EVRC_WB)] = "EVRC_WB"
ConstantAudioQ[str(AUDIO_QUALITY_EVRC_NW)] = "EVRC_NW"
ConstantAudioQ[str(AUDIO_QUALITY_GSM_EFR)] = "GSM_EFR"
ConstantAudioQ[str(AUDIO_QUALITY_GSM_FR)] = "GSM_FR"
ConstantAudioQ[str(AUDIO_QUALITY_GSM_HR)] = "GSM_HR"
ConstantAudioQ[str(AUDIO_QUALITY_G711U)] = "G711u"
ConstantAudioQ[str(AUDIO_QUALITY_G723)] = "G723"
ConstantAudioQ[str(AUDIO_QUALITY_G711A)] = "G711A"
ConstantAudioQ[str(AUDIO_QUALITY_G722)] = "G722"
ConstantAudioQ[str(AUDIO_QUALITY_G711AB)] = "G711AB"
ConstantAudioQ[str(AUDIO_QUALITY_G729)] = "G729"
ConstantAudioQ[str(AUDIO_QUALITY_EVS_NB)] = "EVS_NB"
ConstantAudioQ[str(AUDIO_QUALITY_EVS_WB)] = "EVS_WB"
ConstantAudioQ[str(AUDIO_QUALITY_EVS_SWB)] = "EVS_SWB"
ConstantAudioQ[str(AUDIO_QUALITY_EVS_FB)] = "EVS_FB"

#video info
VIDEO_QUALITY_NONE = 0
VIDEO_QUALITY_QCIF = 1 << 0
VIDEO_QUALITY_QVGA_LANDSCAPE = 1 << 1
VIDEO_QUALITY_QVGA_PORTRAIT = 1 << 2
VIDEO_QUALITY_VGA_LANDSCAPE = 1 << 3
VIDEO_QUALITY_VGA_PORTRAIT = 1 << 4
ConstantVideoQ = dict()
ConstantVideoQ[str(VIDEO_QUALITY_NONE)] = "None Video"
ConstantVideoQ[str(VIDEO_QUALITY_QCIF)] = "QCIF"
ConstantVideoQ[str(VIDEO_QUALITY_QVGA_LANDSCAPE)] = "QVGA_LANDSCAPE"
ConstantVideoQ[str(VIDEO_QUALITY_QVGA_PORTRAIT)] = "QVGA_PORTRAIT"
ConstantVideoQ[str(VIDEO_QUALITY_VGA_LANDSCAPE)] = "VGA_LANDSCAPE"
ConstantVideoQ[str(VIDEO_QUALITY_VGA_PORTRAIT)] = "VGA_PORTRAIT"

#VT config in ImsConfigImpl.java
VT_RESOLUTION_720P = 0
VT_RESOLUTION_VGA_REVERSED_15 = 1
VT_RESOLUTION_VGA_REVERSED_30 = 2
VT_RESOLUTION_QVGA_REVERSED_15 = 3
VT_RESOLUTION_QVGA_REVERSED_30 = 4
VT_RESOLUTION_CIF = 5
VT_RESOLUTION_QCIF = 6
VT_RESOLUTION_VGA_15 = 7
VT_RESOLUTION_VGA_30 = 8
VT_RESOLUTION_QVGA_15 = 9
VT_RESOLUTION_QVGA_30 = 10
ConstantVTResolution = dict()
ConstantVTResolution[str(VT_RESOLUTION_720P)] = "1280x720x30"
ConstantVTResolution[str(VT_RESOLUTION_VGA_REVERSED_15)] = "480x640x15"
ConstantVTResolution[str(VT_RESOLUTION_VGA_REVERSED_30)] = "480x640x30"
ConstantVTResolution[str(VT_RESOLUTION_QVGA_REVERSED_15)] = "240x320x15"
ConstantVTResolution[str(VT_RESOLUTION_QVGA_REVERSED_30)] = "240x320x30"
ConstantVTResolution[str(VT_RESOLUTION_CIF)] = "352x288x30"
ConstantVTResolution[str(VT_RESOLUTION_QCIF)] = "176x144x30"
ConstantVTResolution[str(VT_RESOLUTION_VGA_15)] = "640x480x15"
ConstantVTResolution[str(VT_RESOLUTION_VGA_30)] = "640x480x30"
ConstantVTResolution[str(VT_RESOLUTION_QVGA_15)] = "320x240x15"
ConstantVTResolution[str(VT_RESOLUTION_QVGA_30)] = "320x240x30"


#msg id in ImsConnectionManagerService.java
ConstantImsReq = dict()
ConstantImsReq['MSG_PROCESSING_LOOP'] = "LOOP"
ConstantImsReq['MSG_SWITCH_TO_VOWIFI'] = "Switch to VoWiFi"
ConstantImsReq['MSG_SWITCH_TO_VOLTE'] = "Switch to VoLTE"
ConstantImsReq['MSG_HANDOVER_TO_VOWIFI'] = "Handover to VoWiFi"
ConstantImsReq['MSG_HANDOVER_TO_VOLTE'] = "Handover to VoLTE"
ConstantImsReq['MSG_HANDOVER_TO_VOLTE_BY_TIMER'] = "Handover to VoLTE By Timer"
ConstantImsReq['MSG_RELEASE_VOWIFI_RES'] = "Release VoWiFi Res"
ConstantImsReq['MSG_VOWIFI_UNAVAILABLE'] = "VoWiFi Unavailable"
ConstantImsReq['MSG_CANCEL_CURRENT_REQUEST'] = "Cancel Current Request"