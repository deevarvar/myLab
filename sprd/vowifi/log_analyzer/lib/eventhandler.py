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

class eventhandler():
    def __init__(self, match, color, groupnum):
        self.match = match
        self.color = color
        self.groupnum = groupnum
        self.retmsg = eventdict()
        #set the selected color
        self.retmsg.color = color

    def handler(self):
        #need to overwrite the handler.
        return None

    '''
       ######### main process #########
    '''
    def getret(self):
        grouplen = len(self.match.groups())
        if self.match and grouplen >= self.groupnum:
            return self.handler()
        else:
            return None

class demoinherit(eventhandler):
    def handler(self):
        self.retmsg = self.match.group(1).strip()
        return self.retmsg

#NOTE: color can be set from function input , or defined in function logic
class matchone(eventhandler):
    '''
    only match one , return one
    '''
    def handler(self):
        self.retmsg.msg = self.match.group(1)
        return self.retmsg

class oneclickconf(eventhandler):
    '''
    the one click conf participants, one pattern
    '''
    def handler(self):
        partner = str(self.match.group(1)).strip()
        self.retmsg.msg = "Start Conf with " + partner
        return self.retmsg

class acceptcall(eventhandler):
    '''
    accept call , one pattern, calltype
    '''
    def handler(self):
        calltype = Constantcalltype[str(self.match.group(1).strip())]
        self.retmsg.msglevel = Msglevel.WARNING
        self.retmsg.color = maplevel2color(self.retmsg.msglevel)
        self.retmsg.msg = "Accept As " + calltype
        return self.retmsg

class rejectcall(eventhandler):
    '''
    reject call,
    '''
    def handler(self):
        rejectreason = Constantimsreason[str(self.match.group(1).strip())]
        self.retmsg.msg = "Reject As :" + rejectreason
        return self.retmsg


class startcall(eventhandler):
    '''
    imsservice start call : one pattern
    VoWiFiCall/VoLTECall
    '''
    def handler(self):
        callbearer = self.match.group(1)
        self.retmsg.msg = "start " + callbearer
        return self.retmsg



class servicecallback(eventhandler):
    '''
    complex handler to parse #####Vowifiserservice.java######
    the pattern is only one, the callback json
    sample:
    Notify the event: {"event_code":104,"event_name":"call_talking","id":2,"phone_num":"+917011821207","is_video":false}
    Notify the event: {"event_code":105,"event_name":"call_terminate","id":3,"state_code":335}
    Notify the event: {"event_code":110,"event_name":"call_hold_received","id":2}
    Notify the event: {"event_code":302,"event_name":"remote_video_resize","video_width":240,"video_height":320}
    Notify the event:  {"event_code":103,"event_name":"call_alerted","alert_type":57899,"id":3,"phone_num":"+917011821207","is_video":true}
    Notify the event: {"event_code":118,"event_name":"call_rtp_received","id":1,"rtp_received":true,"is_video":false}
    Notify the event: {"event_code":209,"event_name":"conf_part_update","id":23,"phone_num":"+917011821118","sip_uri":"sip:+917011821118@ims.mnc872.mcc405.3gppnetwork.org","conf_part_new_status":"disconnected"}
    '''
    def handler(self):
        servicestr = self.match.group(1).strip()
        servicejson = json.loads(servicestr)
        #event_name is must
        #enumerate the key in Constants.java
        eventstr = termreason = callidstr = alertstr = isvideostr = phonenumstr = sipuristr = ''
        videohight = videowidth = videoorient = rtprecv = confpartstatus = ''
        msgstr = ''
        #there will event skipped, which means other key will have better phrase
        skipevent = list()
        skipevent.append('call_terminate')
        skipevent.append('call_rtp_received')

        #event to be ignored, like rtcp changed
        ignoreevent = list()
        ignoreevent.append('call_rtcp_changed')
        ignoreevent.append('conf_rtcp_changed')

        #event should be colored blue
        infoevent = list()
        infoevent.append("call_incoming")
        infoevent.append("call_talking")
        infoevent.append("call_terminate") #actually it is skipped
        infoevent.append("call_hold_ok")
        infoevent.append("call_resume_ok")
        infoevent.append("call_hold_received")
        infoevent.append("call_resume_received")
        infoevent.append("call_add_video_ok")
        infoevent.append("call_remove_video_ok")
        infoevent.append("call_add_video_request")
        infoevent.append("call_add_video_cancel")
        infoevent.append("call_rtp_received") #actually it is skipped
        infoevent.append("call_is_focus")
        infoevent.append("conf_connected")
        infoevent.append("conf_disconnected")
        infoevent.append("conf_invite_accept")
        infoevent.append("conf_kick_accept")
        infoevent.append("conf_part_update")
        infoevent.append("conf_hold_ok")
        infoevent.append("conf_resume_ok")
        infoevent.append("conf_hold_received")
        infoevent.append("conf_resume_received")

        #event should be colored red
        errevent = list()
        errevent.append("call_hold_failed")
        errevent.append("call_resume_failed")
        errevent.append("call_add_video_failed")
        errevent.append("call_remove_video_failed")
        errevent.append("conf_invite_failed")
        errevent.append("conf_kick_failed")
        errevent.append("conf_hold_failed")
        errevent.append("conf_resume_failed")

        if 'event_name' in servicejson:
            curevent = str(servicejson['event_name']).strip()
            #rtcp changed is too verbose , so ignore it.
            if curevent in ignoreevent:
                return None

            if curevent not in skipevent:
                #some event should be highlighted
                #just change the color here, phrase is not converted.
                if curevent in infoevent:
                    self.retmsg.msglevel = Msglevel.WARNING
                    self.retmsg.color = maplevel2color(self.retmsg.msglevel)
                elif curevent in errevent:
                    self.retmsg.msglevel = Msglevel.ERROR
                    self.retmsg.color = maplevel2color(self.retmsg.msglevel)

                eventstr = 'Event: ' + curevent + '\n'
            if servicejson['event_name'] == "call_terminate":
                if 'state_code' in servicejson:
                    termreason = 'Term Call: ' + Constantimsreason[str(servicejson['state_code'])] + '\n'
                    self.retmsg.msglevel = Msglevel.WARNING
                    self.retmsg.color = maplevel2color(self.retmsg.msglevel)

            if servicejson['event_name'] == "call_rtp_received":
                if 'rtp_received' in servicejson:
                    #python will convert true to True, false to False
                    rtpstate = str(servicejson['rtp_received']).lower()
                    if rtpstate == 'true':
                        rtprecv = "RTP received\n"
                    else:
                        #show error msg.
                        self.retmsg.msglevel = Msglevel.ERROR
                        self.retmsg.color = maplevel2color(self.retmsg.msglevel)
                        rtprecv = "No RTP received\n"


        if 'id' in servicejson:
            callidstr = "Callid: " + str(servicejson['id']) + '\n'
        if 'alert_type' in servicejson:
            alertstr = "User Alert: " + Constantcallcode[str(servicejson['alert_type'])] + '\n'
        if 'is_video' in servicejson:
            if str(servicejson['is_video']).lower() == "false":
                isvideostr = "calltype: Voice Call\n"
            else:
                isvideostr = "calltype: Video Call\n"
        if 'phone_num' in servicejson:
            phonenumstr = "PhoneNum :" + servicejson['phone_num'] + '\n'
        if 'sip_uri' in servicejson:
            #seems not useful, so comment here
            #sipuristr = "SIP URI :" + servicejson['sip_uri'] + '\n'
            sipuristr = ''
        if 'video_height' in servicejson:
            videohight = "Video Height :" + str(servicejson['video_height']) + '\n'
        if 'video_width' in servicejson:
            videowidth = "Video Width :" + str(servicejson['video_width']) + '\n'
        if 'video_orientation' in servicejson:
            #seems dead code ... Orz~
            pass
        if 'conf_part_new_status' in servicejson:
            confpartstatus = "Conf Part State: " + str(servicejson['conf_part_new_status'])
        #assemble the str
        self.retmsg.msg = eventstr + rtprecv + termreason + callidstr + alertstr + isvideostr + phonenumstr + sipuristr + \
                     videohight + videowidth + videoorient + confpartstatus
        return self.retmsg

class loginstatus(eventhandler):
    '''
    login status, two patterns: ip, pcscf ip
    '''
    def handler(self):
        ip = self.match.group(1).strip()
        pcscfip = self.match.group(2).strip()
        ipstr = "IP: " + ip + '\n'
        pcscfipstr = "P-CSCF: " + pcscfip + '\n'
        self.retmsg.msg = 'Login \n' + ipstr + pcscfipstr
        return self.retmsg


class logoutstatus(eventhandler):
    '''
    logout pattern: Constantregstate
    '''
    def handler(self):
        regstr = Constantregstate[(str(self.match.group(1)).strip())]
        self.retmsg.msglevel = Msglevel.WARNING
        self.retmsg.color = maplevel2color(self.retmsg.msglevel)
        self.retmsg.msg = "Try to Logout \n"+"RegState is " + regstr
        return self.retmsg

class drstatus(eventhandler):
    '''
    data route pattern, one: volte/vowifi/none
    '''
    def handler(self):
        drstate = str(self.match.group(1))
        drstr = "Update data router to "+drstate
        self.retmsg.msglevel = Msglevel.INFO
        self.retmsg.color = maplevel2color(self.retmsg.msglevel)
        self.retmsg.msg = drstr
        return self.retmsg


class wfcstatus(eventhandler):
    '''
    wificalling flag, one pattern
    database has changed, mIsWifiCallingEnabled = true
    '''
    def handler(self):
        wfcdb = str(self.match.group(1))
        wfcstr = ""
        if wfcdb == "true":
            wfcstr = "WiFi-Calling is Enabled"
        else:
            wfcstr = "WiFi-Calling is Disabled"

        self.retmsg.msglevel = Msglevel.WARNING
        self.retmsg.color = maplevel2color(self.retmsg.msglevel)
        self.retmsg.msg = wfcstr
        return self.retmsg

class geticon(eventhandler):
    '''
    get vowifi/volte icon
    '''
    def handler(self):
        ltestr = self.match.group(1)
        wifistr = self.match.group(2)
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
        self.retmsg.msg = iconstr
        self.retmsg.level = level
        self.retmsg.color = maplevel2color(self.retmsg.level)
        return self.retmsg

class imsregaddr(eventhandler):
    '''
    set ims reg addr, one pattern
    '''
    def handler(self):
        regaddr = self.match.group(1)
        self.retmsg.msg = "SetIMSRegAddr:\n   " + regaddr
        return self.retmsg


class mutestatus(eventhandler):
    '''
    mute status: one pattern
    true muted; false unmute
    '''
    def handler(self):
        muteval = str(self.match.group(1))
        self.retmsg.msglevel = Msglevel.WARNING
        self.sg.color = maplevel2color(self.retmsg.msglevel)
        if muteval == 'true':
            self.retmsg.msg = "Muted"
        else:
            self.retmsg.msg = "UnMuted"

        return self.retmsg


class makecallstatus(eventhandler):
    '''
    make call , one pattern , callee number
    '''
    def handler(self):
        callee = str(self.match.group(1)).strip()
        self.retmsg.msglevel = Msglevel.WARNING
        self.retmsg.color = maplevel2color(self.retmsg.msglevel)
        self.retmsg.msg = "Make call to " + callee
        return self.retmsg


class akastatus(eventhandler):
    '''
    aka status
    one pattern DB means auth correctly, DC means sync failure
    '''
    def handler(self):
        akatag = self.match.group(1)
        if akatag == "DB":
            akastr = "AKA AUTH correctly"
            self.retmsg.msglevel = Msglevel.INFO
            self.retmsg.color = maplevel2color(self.retmsg.msglevel)
            self.retmsg.msg = akastr
            return self.retmsg
        elif akatag == "DC":
            akastr = "AKA AUTH SYNC Failure"
            self.retmsg.msglevel = Msglevel.ERROR
            self.retmsg.color = maplevel2color(self.retmsg.msglevel)
            self.retmsg.msg = akastr
            return self.retmsg
        else:
            return None


class reregstatus(eventhandler):
    '''
    re-register info, two pattern: access type and access info
    '''
    def handler(self):
        acctype = Constantaccnettype[str(self.match.group(1).strip())]
        accinfo = self.match.group(2)
        self.retmsg.msglevel = Msglevel.WARNING
        self.retmsg.color = maplevel2color(self.retmsg.msglevel)
        acctypestr = "Access Type:" + acctype + '\n'
        accinfostr =  "Access Info:" + accinfo + '\n'
        self.retmsg.msg = "start to Re-Register\n" + acctypestr + accinfostr
        return self.retmsg


class regstatus(eventhandler):
    '''
    Get the register state changed callback: {\"event_code\":.*,\"event_name\":\"(.*)\",\"state_code\":(.*)}"
    event name , state code
    '''
    def handler(self):
        eventname = self.match.group(1)
        statecode = int(self.match.group(2))
        regbase = int(MTC_CLI_REG_BASE)
        #only return when statecode >= 0xE100 or -1
        if statecode > regbase:
            self.retmsg.level = Msglevel.ERROR
            self.retmsg.color = maplevel2color(self.retmsg.level)
            eventstr = "Register event: " + eventname + '\n'
            statestr = "state: " + Constantregerrcode[str(statecode)]
            self.retmsg.msg = eventstr + statestr
            return self.retmsg
        elif statecode == -1:
            #in service's log, -1 is default value , which means good~
            self.retmsg.level = Msglevel.WARNING
            self.retmsg.color = maplevel2color(self.retmsg.level)
            eventstr = "Register event: " + eventname + '\n'
            self.retmsg.msg = eventstr
            return self.retmsg
        else:
            return None


class s2bstatus(eventhandler):
    '''
    s2b status check
    three kinds:
    {"security_json_action":"security_json_action_s2b_failed","security_json_param_error_code":53760}
    {"security_json_action":"security_json_action_s2b_stopped","security_json_param_error_code":53959,"security_json_param_handover":true}
    {"security_json_action":"security_json_action_s2b_successed","security_json_param_local_ip4":"192.168.1.11","security_json_param_local_ip6":"2001:0:0:2::1","security_json_param_pcscf_ip4":"192.168.1.12;","security_json_param_pcscf_ip6":"2001:0:0:2::2;","security_json_param_dns_ip4":"0.0.0.0","security_json_param_pref_ip4":false}
    '''
    def handler(self):
        #input str is ALWAYS json string.
        s2bstr = self.match.group(1).strip()
        s2bjson = json.loads(s2bstr)
        action = s2bjson['security_json_action']
        if action == 'security_json_action_s2b_failed':
            errorcode = s2bjson['security_json_param_error_code']
            statestr = "epdg attach failed\n"
            errorstr = "   stateCode: " + Constants2berrcode[str(errorcode)]
            self.retmsg.level = Msglevel.ERROR
            self.retmsg.color = maplevel2color(self.retmsg.level)
            self.retmsg.msg = statestr + errorstr
        elif action == "security_json_action_s2b_stopped":
            errorcode = s2bjson['security_json_param_error_code']
            ishandover = s2bjson['security_json_param_handover']
            statestr = "epdg attach stopped\n"
            #add three spaces for alignment, not working...Orz...
            hostr = " ishandover: " + str(ishandover) + '\n'
            errorstr = " StateCode: " + Constants2berrcode[str(errorcode)]
            self.retmsg.level = Msglevel.WARNING
            self.retmsg.color = maplevel2color(self.retmsg.level)
            self.retmsg.msg = statestr + hostr + errorstr
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
            self.retmsg.level = Msglevel.WARNING
            self.retmsg.color = maplevel2color(self.retmsg.level)
            self.retmsg.msg = statestr + ipv4str + ipv6str + pcscfv4str + pcscfv6str + dnsv4 + dnsv6
        else:
            return None

        return self.retmsg


if __name__ == '__main__':
    key = 'abc'
    line = "abc"
    pattern = re.compile(key)
    match = pattern.search(line)
    color = "black"

    print matchone(match, color)
    demohandler =  demoinherit(match, "black", 1)
    print demohandler.getret()