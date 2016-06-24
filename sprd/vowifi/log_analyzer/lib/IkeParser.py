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
            self.ikeheaderpattern = config['sprd']['iketags']
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

        action = match.group(1) #Encode
        content = match.group(2) #IKE_SA_INIT
        msgid = match.group(3)
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