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


if __name__ == '__main__':
    ip = IkeParser()
    ikeheader = "06-23 12:31:44.247  2039  2127 D LEMON   : 12:31:44.247 SECURITY IKE: INFO: Encode: <IKE_SA_INIT>(MsgId:0) Msg Header"
    ip.getIkeHeader(ikeheader)
    ikenewheader ="07-02 18:29:41.844  2141  2197 D LEMON   : 18:29:41.844 SECURITY IKE: INFO: Decode: Exchange Type: <IKE_SA_INIT>(Message ID: 0x00000001) Msg Header"
    ip.getIkeHeader(ikenewheader)