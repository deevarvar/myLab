#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
#some event helper for searchEvent in flowParser.py


import re
import json
from sprdErrCode import *

class Msglevel():
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

def maplevel2color(level):
    if level <= Msglevel.INFO:
        return "black";
    elif level == Msglevel.WARNING:
        return "blue"
    else:
        return "red"

class eventdict():
    def __init__(self):
        self.msglevel = Msglevel.INFO
        self.color = "black"
        self.msg = None


def matchone(match):
    '''
    return the first match one
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    retmsg = eventdict()
    if match and grouplen >= 1:
        retmsg.msg = match.group(1)
        return retmsg
    else:
        return None

def geticon(match):
    '''
    get vowifi/volte icon
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    iconstr = None
    level = Msglevel.INFO
    retmsg = eventdict()
    if match and grouplen >=2:
        ltestr = match.group(1)
        wifistr = match.group(2)
        if ltestr == "true":
            if wifistr == "true":
                iconstr = "show VoWiFi and VoLTE signal icons"
                level = Msglevel.ERROR
            else:
                iconstr = "show VoLTE signal icon"
                level = Msglevel.WARNING

        else:
            if wifistr == "true":
                iconstr = "show VoWiFi signal icon"
                level = Msglevel.WARNING
            else:
                iconstr = "No VoLTE/VoWiFi signal icon"
                level = Msglevel.WARNING
        retmsg.msg = iconstr
        retmsg.level = level
        retmsg.color = maplevel2color(retmsg.level)
        return retmsg
    else:
        return None

def imsregaddr(match):
    '''
    set ims reg addr
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    retmsg = eventdict()
    if match and grouplen >= 1:
        regaddr = match.group(1)
        retmsg.msg = "SetIMSRegAddr:\n   " + regaddr
        return retmsg
    else:
        return None

def regstatus(match):
    '''
    Get the register state changed callback: {\"event_code\":.*,\"event_name\":\"(.*)\",\"state_code\":(.*)}"
    event name , state code
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    retmsg = eventdict()
    if match and grouplen >= 2:
        eventname = match.group(1)
        statecode = int(match.group(2))
        regbase = int(MTC_CLI_REG_BASE)
        #only return when statecode >= 0xE100 or -1
        if statecode > regbase:
            retmsg.level = Msglevel.ERROR
            retmsg.color = maplevel2color(retmsg.level)
            eventstr = "Register event: " + eventname + '\n'
            statestr = "state: " + regerrcode[str(statecode)]
            retmsg.msg = eventstr + statestr
            return retmsg
        elif statecode == -1:
            #in service's log, -1 is default value , which means good~
            retmsg.level = Msglevel.WARNING
            retmsg.color = maplevel2color(retmsg.level)
            eventstr = "Register event: " + eventname + '\n'
            retmsg.msg = eventstr
            return retmsg
        else:
            return None
    else:
        return None

def s2bstatus(match):
    '''
    s2b status check
    three kinds:
    {"security_json_action":"security_json_action_s2b_failed","security_json_param_error_code":53760}
    {"security_json_action":"security_json_action_s2b_stopped","security_json_param_error_code":53959,"security_json_param_handover":true}
    {"security_json_action":"security_json_action_s2b_successed","security_json_param_local_ip4":"192.168.1.11","security_json_param_local_ip6":"2001:0:0:2::1","security_json_param_pcscf_ip4":"192.168.1.12;","security_json_param_pcscf_ip6":"2001:0:0:2::2;","security_json_param_dns_ip4":"0.0.0.0","security_json_param_pref_ip4":false}
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    retmsg = eventdict()
    if match and grouplen >= 1:
        #input str is ALWAYS json string.
        s2bstr = match.group(1)
        s2bjson = json.loads(s2bstr)
        action = s2bjson['security_json_action']
        if action == 'security_json_action_s2b_failed':
            errorcode = s2bjson['security_json_param_error_code']
            statestr = "epdg attach failed\n"
            errorstr = "   stateCode: " + s2berrcode[str(errorcode)]
            retmsg.level = Msglevel.ERROR
            retmsg.color = maplevel2color(retmsg.level)
            retmsg.msg = statestr + errorstr
        elif action == "security_json_action_s2b_stopped":
            errorcode = s2bjson['security_json_param_error_code']
            ishandover = s2bjson['security_json_param_handover']
            statestr = "epdg attach stopped\n"
            #add three spaces for alignment, not working...Orz...
            hostr = " ishandover: " + str(ishandover) + '\n'
            errorstr = " StateCode: " + s2berrcode[str(errorcode)]
            retmsg.level = Msglevel.WARNING
            retmsg.color = maplevel2color(retmsg.level)
            retmsg.msg = statestr + hostr + errorstr
        elif action == "security_json_action_s2b_successed":
            statestr = "epdg attach successfully\n"
            ipv4str = ipv6str = pcscfv4str = pcscfv6str = dnsv4 = dnsv6 = ''
            if 'security_json_param_local_ip4' in s2bjson:
                ipv4str = "     IPv4: " + s2bjson['security_json_param_local_ip4'] + '\n'
            if 'security_json_param_local_ip6' in s2bjson:
                ipv6str = "     IPv6: " + s2bjson['security_json_param_local_ip6'] + '\n'
            if 'security_json_param_pcscf_ip4' in s2bjson:
                pcscfv4str = "   PCSCF IPv4: " + s2bjson['security_json_param_pcscf_ip4'] + '\n'
            if 'security_json_param_pcscf_ip6' in s2bjson:
                pcscfv6str = "   PCSCF IPv6: " + s2bjson['security_json_param_pcscf_ip6'] + '\n'
            if 'security_json_param_dns_ip4' in s2bjson:
                dnsv4str = "   DNS IPv4: " + s2bjson['security_json_param_dns_ip4'] + '\n'
            if 'security_json_param_dns_ip6' in s2bjson:
                dnsv4str = "   DNS IPv6: " + s2bjson['security_json_param_dns_ip6'] + '\n'
            retmsg.level = Msglevel.WARNING
            retmsg.color = maplevel2color(retmsg.level)
            retmsg.msg = statestr + ipv4str + ipv6str + pcscfv4str + pcscfv6str + dnsv4 + dnsv6
        else:
            return None

        return retmsg

    else:
        return None

if __name__ == '__main__':
    key = 'abc'
    line = "abc"
    pattern = re.compile(key)
    match = pattern.search(line)
    print matchone(match)