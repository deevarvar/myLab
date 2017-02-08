#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
# error code mapping for service and IKE
#log pattern:   code: 576|errorCode: 537
#definition:    mtc_cli.h, mtc_s2b.h

#defined in vowifisecuritymanager.java
#security_json_action_s2b_successed, security_json_action_s2b_failed, security_json_action_s2b_stopped
#D:\code\log\india_2016_8_24\bugs\592271\No_Volte_Icon_Idle


Constantregstatecode = dict()
MTC_CLI_STATE_IDLE=0
MTC_CLI_STATE_REGING=1
EN_MTC_CLI_STATE_LOGINED=2
EN_MTC_CLI_STATE_UNREGING=3
Constantregstatecode[str(int(MTC_CLI_STATE_IDLE))] = "IDLE"
Constantregstatecode[str(int(MTC_CLI_STATE_REGING))] = "REGING"
Constantregstatecode[str(int(EN_MTC_CLI_STATE_LOGINED))] = "LOGINED"
Constantregstatecode[str(int(EN_MTC_CLI_STATE_UNREGING))] = "UNREGING"


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
Constants2berrcode[str(int(MTC_S2B_BASE+197))] = "IKE Ping Error"
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
EN_MTC_ACC_NET_3GPP_E_UTRAN_TDD = 10
Constantaccnettype[str(EN_MTC_ACC_NET_IEEE_802_11)] = "IEEE-802.11"
Constantaccnettype[str(EN_MTC_ACC_NET_3GPP_E_UTRAN_FDD)] = "3GPP-E-UTRAN-FDD"
Constantaccnettype[str(EN_MTC_ACC_NET_3GPP_E_UTRAN_TDD)] = "3GPP-E-UTRAN-TDD"

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


#security code
Constantikeroaming = dict()
ROAMING_TYPE_NOT_ROAMING = 0
ROAMING_TYPE_UNKNOWN = 1
ROAMING_TYPE_DOMESTIC = 2
ROAMING_TYPE_INTERNATIONAL = 3
Constantikeroaming[str(ROAMING_TYPE_NOT_ROAMING)] = "not roaming"
Constantikeroaming[str(ROAMING_TYPE_UNKNOWN)] = "unknow"
Constantikeroaming[str(ROAMING_TYPE_DOMESTIC)] = "Domestic"
Constantikeroaming[str(ROAMING_TYPE_INTERNATIONAL)] = "international"

#TelephonyManager.java
ConstantNetworkType = dict()
NETWORK_TYPE_UNKNOWN = 0
NETWORK_TYPE_GPRS = 1
NETWORK_TYPE_EDGE = 2
NETWORK_TYPE_UMTS = 3
NETWORK_TYPE_CDMA = 4
NETWORK_TYPE_EVDO_0 = 5
NETWORK_TYPE_EVDO_A = 6
NETWORK_TYPE_1xRTT = 7
NETWORK_TYPE_HSDPA = 8
NETWORK_TYPE_HSUPA = 9
NETWORK_TYPE_HSPA = 10
NETWORK_TYPE_IDEN = 11
NETWORK_TYPE_EVDO_B = 12
NETWORK_TYPE_LTE = 13
NETWORK_TYPE_EHRPD = 14
NETWORK_TYPE_HSPAP = 15
NETWORK_TYPE_GSM = 16
NETWORK_TYPE_TD_SCDMA = 17
NETWORK_TYPE_IWLAN = 18
NETWORK_TYPE_LTE_CA = 19

ConstantNetworkType[str(NETWORK_TYPE_UNKNOWN)] = "Unknown"
ConstantNetworkType[str(NETWORK_TYPE_GPRS)] = "GPRS"
ConstantNetworkType[str(NETWORK_TYPE_EDGE)] = "EDGE"
ConstantNetworkType[str(NETWORK_TYPE_UMTS)] = "UMTS"
ConstantNetworkType[str(NETWORK_TYPE_CDMA)] = "CDMA"
ConstantNetworkType[str(NETWORK_TYPE_EVDO_0)] = "EVDO_0"
ConstantNetworkType[str(NETWORK_TYPE_EVDO_A)] = "EVDO_A"
ConstantNetworkType[str(NETWORK_TYPE_1xRTT)] = "1xRTT"
ConstantNetworkType[str(NETWORK_TYPE_HSDPA)] = "HSDPA"
ConstantNetworkType[str(NETWORK_TYPE_HSUPA)] = "HSUPA"
ConstantNetworkType[str(NETWORK_TYPE_HSPA)] = "HSPA"
ConstantNetworkType[str(NETWORK_TYPE_IDEN)] = "IDEN"
ConstantNetworkType[str(NETWORK_TYPE_EVDO_B)] = "EVDO_B"
ConstantNetworkType[str(NETWORK_TYPE_LTE)] = "LTE"
ConstantNetworkType[str(NETWORK_TYPE_EHRPD)] = "EHRPD"
ConstantNetworkType[str(NETWORK_TYPE_HSPAP)] = "HSPAP"
ConstantNetworkType[str(NETWORK_TYPE_GSM)] = "GSM"
ConstantNetworkType[str(NETWORK_TYPE_TD_SCDMA)] = "TD_SCDMA"
ConstantNetworkType[str(NETWORK_TYPE_IWLAN)] = "WLAN"
ConstantNetworkType[str(NETWORK_TYPE_LTE_CA)] = "LTE_CA"

#telephony and adapter's msg
Constanttelemsg = dict()
MSG_RESET = 1
MSG_RESET_FORCE = 2
MSG_ATTACH = 3
MSG_DEATTACH = 4
MSG_REGISTER = 5
MSG_DEREGISTER = 6
MSG_REREGISTER = 7
MSG_UPDATE_DATAROUTER_STATE = 8
MSG_TERMINATE_CALLS = 9
Constanttelemsg[str(MSG_RESET)] = 'Reset'
Constanttelemsg[str(MSG_RESET_FORCE)] = 'Force Reset'
Constanttelemsg[str(MSG_ATTACH)] = 'start Epdg attach'
Constanttelemsg[str(MSG_DEATTACH)] = 'Stop Epdg attach'
Constanttelemsg[str(MSG_REGISTER)] = 'Start VoWiFi Register'
Constanttelemsg[str(MSG_DEREGISTER)] = 'Start VoWiFi De-Register'
Constanttelemsg[str(MSG_REREGISTER)] = 'Start Re-Register'
Constanttelemsg[str(MSG_UPDATE_DATAROUTER_STATE)] = 'Update DataRouter'
Constanttelemsg[str(MSG_TERMINATE_CALLS)] = 'Term Call'

#sms error code MtcImConstants.java
ConstantImmsg = dict()

MTC_IM_ERR_NO = (0xEA00+0) # /**< @brief no error. */
ConstantImmsg[str(MTC_IM_ERR_NO)]   = "No error"
MTC_IM_ERR_AUTH_FAILED = (0xEA00+1)#/**< @brief authentication failed, invalid user or password. */
ConstantImmsg[str(MTC_IM_ERR_AUTH_FAILED)] = "Auth Failed"
MTC_IM_ERR_SESS_TMR = (0xEA00+2) #/**< @brief im session refresh error. */
ConstantImmsg[str(MTC_IM_ERR_SESS_TMR)] = "Session Refresh Error"
MTC_IM_ERR_FORBIDDEN = (0xEA00+3)# /**< @brief im forbidden. */
ConstantImmsg[str(MTC_IM_ERR_FORBIDDEN)] = "Forbidden"
MTC_IM_ERR_NOT_FOUND = (0xEA00+4)#/**< @brief im participant not found. */
ConstantImmsg[str(MTC_IM_ERR_NOT_FOUND)] = "Participant not found"
MTC_IM_ERR_NOT_ACPTED = (0xEA00+5) #/**< @brief im not accepted. */
ConstantImmsg[str(MTC_IM_ERR_NOT_ACPTED)] = "Not accepted"
MTC_IM_ERR_TEMP_UNAVAIL = (0xEA00+6)# /**< @brief im participant temp unavailable. */
ConstantImmsg[str(MTC_IM_ERR_TEMP_UNAVAIL)] = "Temp Unavailable"
MTC_IM_ERR_REQ_TERMED = (0xEA00+7)# /**< @brief im request terminated. */
ConstantImmsg[str(MTC_IM_ERR_REQ_TERMED)] = "Request terminated"
MTC_IM_ERR_INTERNAL_ERR = (0xEA00+8) #/**< @brief server internal error. */
ConstantImmsg[str(MTC_IM_ERR_INTERNAL_ERR)] = "Server Internal Error"
MTC_IM_ERR_SRV_UNAVAIL = (0xEA00+9)# /**< @brief service unavailable. */
ConstantImmsg[str(MTC_IM_ERR_SRV_UNAVAIL)] = "Server Unavailable"
MTC_IM_ERR_TIMEOUT = (0xEA00+10) #;/**< @brief request timeout. */
ConstantImmsg[str(MTC_IM_ERR_TIMEOUT)] = "Request Timeout"
MTC_IM_ERR_OFFLINE = (0xEA00+11)# /**< @brief callee not registered. */
ConstantImmsg[str(MTC_IM_ERR_OFFLINE)] = "Offline"
MTC_IM_ERR_NETWORK = (0xEA00+12)#/**< @brief network error. */
ConstantImmsg[str(MTC_IM_ERR_NETWORK)] = "Network Error"
MTC_IM_ERR_EXPELLED = (0xEA00+13)# /**< @brief expelled error. */
ConstantImmsg[str(MTC_IM_ERR_EXPELLED)] = "Expelled Error"
MTC_IM_ERR_GONE = (0xEA00+14)# /**< @brief gone. */
ConstantImmsg[str(MTC_IM_ERR_GONE)] = "Gone"
MTC_IM_ERR_EXCEED_MAX_PARTP = (0xEA00+15)# /**< @brief exceed maximum participant size. */
ConstantImmsg[str(MTC_IM_ERR_EXCEED_MAX_PARTP)] = "exceed maximum participant size"
MTC_IM_ERR_EXCEED_MAX_LENGTH = (0xEA00+16)#/**< @brief exceed maximum length. */
ConstantImmsg[str(MTC_IM_ERR_EXCEED_MAX_LENGTH)] = "exceed maximum length"
MTC_IM_ERR_CREATED_GRP_FULL = (0xEA00+17)#/**< @brief created group is full. */
ConstantImmsg[str(MTC_IM_ERR_CREATED_GRP_FULL)] = "created group is full"
MTC_IM_ERR_JOINED_GRP_FULL = (0xEA00+18)#/**< @brief joined group is full. */
ConstantImmsg[str(MTC_IM_ERR_JOINED_GRP_FULL)] = "joined group is full"
MTC_IM_ERR_MANAGED_GRP_FULL = (0xEA00+19)#/**< @brief managed group is full. */
ConstantImmsg[str(MTC_IM_ERR_MANAGED_GRP_FULL)] = "managed group is full"
MTC_IM_ERR_DECLINE = (0xEA00+20)#/**< @brief decline. */
ConstantImmsg[str(MTC_IM_ERR_DECLINE)] = "Decline"
MTC_IM_ERR_TOO_FEW_PARTP = (0xEA00+21)# /**< @brief too few participant. */
ConstantImmsg[str(MTC_IM_ERR_TOO_FEW_PARTP)] = "too few participant"
MTC_IM_ERR_NO_PARTPLST = (0xEA00+22)# /**< @brief no participant list. */
ConstantImmsg[str(MTC_IM_ERR_NO_PARTPLST)] = "no participant list"
MTC_IM_ERR_GRPNAME_NOT_ALLOW = (0xEA00+23)# /**< @brief Group name not allowed by monitor plat. */
ConstantImmsg[str(MTC_IM_ERR_GRPNAME_NOT_ALLOW)] = "Group name not allowed by monitor plat"
MTC_IM_ERR_RESLST_SYNTAX = (0xEA00+24)#/**< @brief Resource-list syntax error. */
ConstantImmsg[str(MTC_IM_ERR_RESLST_SYNTAX)] = "Resource-list syntax errort"
MTC_IM_ERR_REFERTO_REQUIRED = (0xEA00+25)# /**< @brief Refer-To field required. */
ConstantImmsg[str(MTC_IM_ERR_REFERTO_REQUIRED)] = "Refer-To field required"
MTC_IM_ERR_ORIGINATOR_NOTIN_GROUP = (0xEA00+26)# /**< @brief Originator not in group. */
ConstantImmsg[str(MTC_IM_ERR_ORIGINATOR_NOTIN_GROUP)] = "Originator not in group"
MTC_IM_ERR_ALREADY_IN_GROUP = (0xEA00+27)# /**< @brief Destination already in group. */
ConstantImmsg[str(MTC_IM_ERR_ALREADY_IN_GROUP)] = "Destination already in group"
MTC_IM_ERR_SERVER_NOT_AUTHED = (0xEA00+28)# /**< @brief Service not authorised. */
ConstantImmsg[str(MTC_IM_ERR_SERVER_NOT_AUTHED)] = "Service not authorised"
MTC_IM_ERR_PARTP_NOTIN_GROUP = (0xEA00+29)# /**< @brief Destination not in group. */
ConstantImmsg[str(MTC_IM_ERR_PARTP_NOTIN_GROUP)] = "Destination not in group"
MTC_IM_ERR_PARTP_MISS_GPMAN_CAP = (0xEA00+30)# /**< @brief Destination miss gpmanage capability. */
ConstantImmsg[str(MTC_IM_ERR_PARTP_MISS_GPMAN_CAP)] = "Destination miss gpmanage capability"
MTC_IM_ERR_CHAGE_ADMIN_LOOPED = (0xEA00+31)# /**< @brief Change admin oper looped. */
ConstantImmsg[str(MTC_IM_ERR_CHAGE_ADMIN_LOOPED)] = "Change admin oper looped"
MTC_IM_ERR_GRP_MEMBER_FULL = (0xEA00+32)# /**< @brief Group chat is full. */
ConstantImmsg[str(MTC_IM_ERR_GRP_MEMBER_FULL)] = "Group chat is full"
MTC_IM_ERR_GPMESSAGE_NOT_AUTH = (0xEA00+33)# /**< @brief Group SMS Message have no authority. */
ConstantImmsg[str(MTC_IM_ERR_GPMESSAGE_NOT_AUTH)] = "Group SMS Message have no authority"
MTC_IM_ERR_GPMESSAGE_OUT_QUOTA = (0xEA00+34)# /**< @brief Group SMS Message out of quota */
ConstantImmsg[str(MTC_IM_ERR_GPMESSAGE_OUT_QUOTA)] = "Group SMS Message out of quota"
MTC_IM_ERR_GPMESSAGE_VIP_OUT_QUOTA = (0xEA00+35)# /**< @brief Group SMS Message vip out of quota */
ConstantImmsg[str(MTC_IM_ERR_GPMESSAGE_VIP_OUT_QUOTA)] = "Group SMS Message vip out of quota"
MTC_IM_ERR_GPMESSAGE_SAFETY_OUT_QUOTA = (0xEA00+36)# /**< @brief Group SMS Message safety out of quota */
ConstantImmsg[str(MTC_IM_ERR_GPMESSAGE_SAFETY_OUT_QUOTA)] = "roup SMS Message safety out of quota"
MTC_IM_ERR_NOT_REGED = (0xEA00+37)# /**< @brief not registered */
ConstantImmsg[str(MTC_IM_ERR_NOT_REGED)] = "Not Registered"
MTC_IM_ERR_PROC_AUTH_CHANLLENGE = (0xEA00+38)# /**< @brief process 407 */
ConstantImmsg[str(MTC_IM_ERR_PROC_AUTH_CHANLLENGE)] = "Process 407"
MTC_IM_ERR_CREATE_SIP_MSG = (0xEA00+39)#/**< @brief create sip message */
ConstantImmsg[str(MTC_IM_ERR_CREATE_SIP_MSG)] = "create sip message"
MTC_IM_ERR_OTHER = (0xEA00+200)# /**< @brief other error. */
ConstantImmsg[str(MTC_IM_ERR_OTHER)] = "other error"


#EN_MTC_SMS_TYPE
ConstantSmsType = dict()
EN_MTC_SMS_CONT_UNKNOWN = 0#/**< @brief unknown content */
ConstantSmsType[str(EN_MTC_SMS_CONT_UNKNOWN)] = "Unknow Content"
EN_MTC_SMS_CONT_RPDATA = EN_MTC_SMS_CONT_UNKNOWN + 1# /**< @brief sms rp-data content */
ConstantSmsType[str(EN_MTC_SMS_CONT_RPDATA)] = "RP-DATA content"
EN_MTC_SMS_CONT_RPACK = EN_MTC_SMS_CONT_RPDATA + 1# /**< @brief sms rp-ack content */
ConstantSmsType[str(EN_MTC_SMS_CONT_RPACK)] = "RP-ACK content"
EN_MTC_SMS_CONT_RPSMMA = EN_MTC_SMS_CONT_RPACK + 1# /**< @brief sms rp-smma content */
ConstantSmsType[str(EN_MTC_SMS_CONT_RPSMMA)] = "RP-SMMA content"
EN_MTC_SMS_CONT_RPERROR = EN_MTC_SMS_CONT_RPSMMA + 1#/**< @brief sms rp-error content */
ConstantSmsType[str(EN_MTC_SMS_CONT_RPERROR)] = "RP-ERROR content"
