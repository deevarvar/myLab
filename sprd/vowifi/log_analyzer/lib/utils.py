#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com


import os
import sys
import re
import fnmatch
import errno
import blockdiag
import blockdiag.imagedraw
from blockdiag.noderenderer import box,actor,beginpoint,circle,cloud,diamond,dots
import blockdiag.plugins
from blockdiag.imagedraw import png


sys.path.append('./')
from logConf import logConf
from configobj import ConfigObj,ConfigObjError


class utils():
    def __init__(self, configpath='..'):
        try:
            configfile = configpath + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.logpattern = config['files']['log']

            #all the dirs
            self.dirlist = list()
            dirnames = config['utils']['dirnames']
            dirlist = dirnames.split(' ')
            for index ,dir in enumerate(dirlist):
                self.dirlist.append(dir)

            #singleton logger
            self.logger = logConf()

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)


    def findlogs(self, dirname):
        '''
        find all log files recursively in one given dir
        :return:
        '''
        matches = []
        for root, dirnames, filenames in os.walk(dirname):
            #print root
            #print dirnames
            #print filenames
            for filename in fnmatch.filter(filenames, self.logpattern):
                matches.append(os.path.join(root, filename))
        return matches

    #similar to "mkdir -p"
    def mkdirp(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def createdirs(self, prefix):
        for index, dir in enumerate(self.dirlist):
            fdir = prefix + '/' + dir
            self.mkdirp(fdir)


    '''
        have to init every need ones
    '''
    def setup_imagedraw(self):
        png.setup(png)



    def setup_noderenderers(self):
        box.setup(box)
        actor.setup(actor)
        beginpoint.setup(beginpoint)
        circle.setup(circle)
        cloud.setup(cloud)
        diamond.setup(diamond)
        dots.setup(dots)


if __name__ == '__main__':
    utils = utils()
    matches = utils.findlogs('./src')
    for index,file in enumerate(matches):
        print file