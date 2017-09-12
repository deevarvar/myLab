#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

import os
from configobj import ConfigObj,ConfigObjError
import definition

class config():
    def __init__(self):
        try:
            configfile = definition.CONFIG_PATH + '/config.ini'
            tmpconfig = ConfigObj(configfile, file_error=True)
            self.config = dict()
            self.config['key'] = tmpconfig['keywords']['media']
            self.config['version'] = tmpconfig['utils']['version']
        except (ConfigObjError, IOError) as e:
             print('Could not read "%s": %s' % ('config.ini', e))

    def getmkey(self):
        return self.config['key']


if __name__ == '__main__':
    config = config()
    print config.config['key'], config.config['version']