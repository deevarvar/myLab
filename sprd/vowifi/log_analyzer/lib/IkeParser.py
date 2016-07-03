import os
import sys
import re
from configobj import ConfigObj,ConfigObjError

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('./')
from logConf import logConf
import logging

class IkeParser():
    def __init__(self, configpath='..'):
        try:
            configfile = configpath + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            #there can be two kinds of ike tags
            self.ikeheaderpattern = config['sprd']['iketags'] + '|' + config['sprd']['ikenewtags']
            self.ikespipattern = config['sprd']['ikespitags']
            self.ikev4pattern = config['sprd']['ikev4tags']
            self.ikev6pattern = config['sprd']['ikev6tags']
            self.ikednsv4pattern = config['sprd']['ikednsv4tags']
            self.ikednsv6pattern = config['sprd']['ikednsv6tags']
            self.ikepv6pattern = config['sprd']['ikepcscfv6tags']
            self.ikepv4pattern = config['sprd']['ikepcscfv4tags']

            self.logger = logConf()
        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)

    def getIkeHeader(self, line):
        ikeheaderpattern = re.compile(self.ikeheaderpattern)
        match = ikeheaderpattern.search(line)
        if not match:
            self.logger.logger.debug('no ike header in line ' + line)
            return None
        #SECURITY IKE: INFO: Encode: <IKE_SA_INIT>(MsgId:0) Msg Header
        #SECURITY IKE: INFO: Decode: Exchange Type: <IKE_SA_INIT>(Message ID: 0x00000000) Msg Header
        action = match.group(1) #Encode
        if not action:
            #new ike tags
            action = match.group(4)
            content = match.group(5)
            msgid = match.group(6)
            msgid = str(msgid).lstrip('0')
            if not msgid:
                msgid = '0'
        else:
            #old ike tags
            content = match.group(2) #IKE_SA_INIT
            msgid = match.group(3)
            msgid = str(msgid).lstrip('0')
            if not msgid:
                msgid = '0'
        self.logger.logger.debug('action is ' + action + ', content is ' + content + ', msgid is ' + str(msgid))
        header = dict()
        header['action'] = action
        header['content'] = content
        header['msgid'] = msgid
        return header

    def getikepayload(self, vmsg):
        payload = dict()
        payload['spi'] = dict()
        payload['spi']['spii'] = ''
        payload['spi']['spir'] = ''

        payload['config'] = dict()
        payload['config']['ipv4'] = ''
        payload['config']['ipv6'] = ''
        payload['config']['dnsv4'] = ''
        payload['config']['dnsv6'] = ''
        payload['config']['pcscfipv4_1'] = ''
        payload['config']['pcscfipv4_2'] = ''
        payload['config']['pcscfipv6_1'] = ''
        payload['config']['pcscfipv6_2'] = ''

        spipattern = re.compile(self.ikespipattern)
        v4 = re.compile(self.ikev4pattern)
        v6 =  re.compile(self.ikev6pattern)
        dnsv4 = re.compile(self.ikednsv4pattern)
        dnsv6 = re.compile(self.ikednsv6pattern)
        pv4 = re.compile(self.ikepv4pattern)
        pv6 = re.compile(self.ikepv6pattern)

        foundpv4 = 0
        foundpv6 = 0


        for index, line in enumerate(vmsg):
            #search the pattern
            matchspi = spipattern.search(line)
            if matchspi:
                payload['spi']['spii'] = matchspi.group(1).strip(' ')
                payload['spi']['spir'] = matchspi.group(2).strip(' ')
                self.logger.logger.error('spii is ' + str(payload['spi']['spii']) + ', spir is ' + str(payload['spi']['spir']))

            matchv4 = v4.search(line)
            if matchv4:
                payload['config']['ipv4'] = matchv4.group(1).strip(' ')
                self.logger.logger.error('ipv4 is ' + payload['config']['ipv4'])

            matchv6 = v6.search(line)
            if matchv6:
                payload['config']['ipv6'] = matchv6.group(1).strip(' ')
                self.logger.logger.error('ipv6 is ' + payload['config']['ipv6'])

            matchdnsv4 = dnsv4.search(line)
            if matchdnsv4:
                payload['config']['dnsv4'] = matchdnsv4.group(1).strip(' ')
                self.logger.logger.error('dnsv4 is ' + payload['config']['dnsv4'])

            matchdnsv6 = dnsv6.search(line)
            if matchdnsv6:
                payload['config']['dnsv6'] = matchdnsv6.group(1).strip(' ')
                self.logger.logger.error('ipv6 is ' + payload['config']['dnsv6'])

            #pcscf v4, v6 can be two address for each one...
            matchpv4 = pv4.search(line)
            if matchpv4:
                foundpv4 += 1
                if foundpv4 <= 2:
                    pcscfv4 = "pcscfipv4_" + str(foundpv4)
                    payload['config'][pcscfv4] = matchpv4.group(1).strip(' ')
                    self.logger.logger.error('pcscf v4 is ' + payload['config'][pcscfv4])

            matchpv6 = pv6.search(line)
            if matchpv6:
                foundpv6 += 1
                if foundpv6 <= 2:
                    pcscfv6 = "pcscfipv6_" + str(foundpv6)
                    payload['config'][pcscfv6] = matchpv6.group(1).strip(' ')
                    self.logger.logger.error('pcscf v6 is ' + payload['config'][pcscfv6])

        return payload

if __name__ == '__main__':
    ip = IkeParser()
    ikeheader = "06-23 12:31:44.247  2039  2127 D LEMON   : 12:31:44.247 SECURITY IKE: INFO: Encode: <IKE_SA_INIT>(MsgId:0) Msg Header"
    ip.getIkeHeader(ikeheader)
    ikenewheader ="07-02 18:29:41.844  2141  2197 D LEMON   : 18:29:41.844 SECURITY IKE: INFO: Decode: Exchange Type: <IKE_SA_INIT>(Message ID: 0x00000001) Msg Header"
    ip.getIkeHeader(ikenewheader)