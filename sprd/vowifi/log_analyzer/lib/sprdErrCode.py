#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
# error code mapping for service and IKE
#log pattern:   code: 576|errorCode: 537
#definition:    mtc_cli.h, mtc_s2b.h

#defined in vowifisecuritymanager.java
#security_json_action_s2b_successed, security_json_action_s2b_failed, security_json_action_s2b_stopped
#D:\code\log\india_2016_8_24\bugs\592271\No_Volte_Icon_Idle

Constantregerrcode = dict()
MTC_CLI_REG_BASE=0xE100

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
MTC_S2B_BASE=0xD200
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
STATE_PROGRESSING = 1;
STATE_CONNECTED = 2;
Constantregstate[str(STATE_IDLE)] = "Unreged"
Constantregstate[str(STATE_PROGRESSING)] = "Reging"
Constantregstate[str(STATE_CONNECTED)] = "Reged"


#call type defined in ImsCallProfile.java
Constantcalltype = dict()
CALL_TYPE_VOICE = 2
CALL_TYPE_VT = 4
Constantcalltype[str(CALL_TYPE_VOICE)] = "Voice Call"
Constantcalltype[str(CALL_TYPE_VT)] = "Video Call"


