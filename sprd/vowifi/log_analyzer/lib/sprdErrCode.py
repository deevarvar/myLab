#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
# error code mapping for service and IKE
#log pattern:   code: 576|errorCode: 537
#definition:    mtc_cli.h, mtc_s2b.h

#defined in vowifisecuritymanager.java
#security_json_action_s2b_successed, security_json_action_s2b_failed, security_json_action_s2b_stopped
#D:\code\log\india_2016_8_24\bugs\592271\No_Volte_Icon_Idle

regerrcode = dict()
MTC_CLI_REG_BASE=0xE100

regerrcode[str(int(MTC_CLI_REG_BASE+1))] = "Local request error"
regerrcode[str(int(MTC_CLI_REG_BASE+2))] = "Send message error"
regerrcode[str(int(MTC_CLI_REG_BASE+3))] = "Authentication failed"
regerrcode[str(int(MTC_CLI_REG_BASE+4))] = "Invalid user"
regerrcode[str(int(MTC_CLI_REG_BASE+5))] = "Register timeout"
regerrcode[str(int(MTC_CLI_REG_BASE+6))] = "Register server busy"
regerrcode[str(int(MTC_CLI_REG_BASE+7))] = "Register server not reache"
regerrcode[str(int(MTC_CLI_REG_BASE+8))] = "Register forbidden"
regerrcode[str(int(MTC_CLI_REG_BASE+9))] = "Register unavailable"
regerrcode[str(int(MTC_CLI_REG_BASE+10))] = "Register dns query error"
regerrcode[str(int(MTC_CLI_REG_BASE+11))] = "Register network error"
regerrcode[str(int(MTC_CLI_REG_BASE+12))] = "Register deactived"
regerrcode[str(int(MTC_CLI_REG_BASE+13))] = "Register probation"
regerrcode[str(int(MTC_CLI_REG_BASE+14))] = "Register internal error"
regerrcode[str(int(MTC_CLI_REG_BASE+15))] = "Register no resource"
regerrcode[str(int(MTC_CLI_REG_BASE+16))] = "Other register error"

s2berrcode = dict()
MTC_S2B_BASE=0xD200
s2berrcode[str(int(MTC_S2B_BASE))] = "no error"
s2berrcode[str(int(MTC_S2B_BASE+1))] = "idle error"
s2berrcode[str(int(MTC_S2B_BASE+2))] = "fqdn error"
s2berrcode[str(int(MTC_S2B_BASE+3))] = "sainit error"
s2berrcode[str(int(MTC_S2B_BASE+4))] = "auth error"
s2berrcode[str(int(MTC_S2B_BASE+5))] = "eap error"
s2berrcode[str(int(MTC_S2B_BASE+6))] = "auth finish error"
s2berrcode[str(int(MTC_S2B_BASE+7))] = "auth resend error"
s2berrcode[str(int(MTC_S2B_BASE+8))] = "enter aka error"
s2berrcode[str(int(MTC_S2B_BASE+9))] = "resend timeout error"
s2berrcode[str(int(MTC_S2B_BASE+10))] = "ipsec rekey error"
s2berrcode[str(int(MTC_S2B_BASE+11))] = "IKE rekey error"
s2berrcode[str(int(MTC_S2B_BASE+12))] = "IKE reauth error"
s2berrcode[str(int(MTC_S2B_BASE+13))] = "IKE termining error"
s2berrcode[str(int(MTC_S2B_BASE+14))] = "IKE mobike error"
s2berrcode[str(int(MTC_S2B_BASE+15))] = "IKE dpd error"
s2berrcode[str(int(MTC_S2B_BASE+198))] = "IKE interrupt stop"
s2berrcode[str(int(MTC_S2B_BASE+199))] = "IKE handover stop"
s2berrcode[str(int(MTC_S2B_BASE+200))] = "IKE other error"

#some definition in EN_MTC_ACC_NET_TYPE
accnettype = dict()
EN_MTC_ACC_NET_IEEE_802_11 = 1
EN_MTC_ACC_NET_3GPP_E_UTRAN_FDD = 9
accnettype[str(EN_MTC_ACC_NET_IEEE_802_11)] = "IEEE-802.11"
accnettype[str(EN_MTC_ACC_NET_3GPP_E_UTRAN_FDD)] = "3GPP-E-UTRAN-FDD"

#adapter definition in RegisterState
regstate = dict()
STATE_IDLE = 0
STATE_PROGRESSING = 1;
STATE_CONNECTED = 2;
regstate[str(STATE_IDLE)] = "Unreged"
regstate[str(STATE_PROGRESSING)] = "Reging"
regstate[str(STATE_CONNECTED)] = "Reged"
