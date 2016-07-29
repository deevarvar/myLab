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
from blockdiag.imagedraw import png,pdf,svg


sys.path.append('./')
from logConf import logConf
from configobj import ConfigObj,ConfigObjError
from operator import itemgetter

class utils():
    def __init__(self, configpath='..'):
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
            configfile = configpath + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            #NOTE: logpatten is a list
            self.mlogpattern = config['files']['log']

            self.rlogpattern = config['files']['radiolog']
            self.klogpattern = config['files']['kernellog']

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
        :return: a list of logs including main, kernel,
        '''
        #NOTE: main, kernel, radio have the same format
        #0-main-07-27-12-36-30.log
        #0-radio-07-27-12-36-30.log
        #0-kernel-07-27-12-36-30.log
        matches = list()

        mainmatches = list()
        for root, dirnames, filenames in os.walk(dirname):
            #print root
            #print dirnames
            #print filenames

            for filename in fnmatch.filter(filenames, self.mlogpattern):
                mainmatches.append(os.path.join(root, filename))

        radiomatches = list()
        for root, dirnames, filenames in os.walk(dirname):
            #print root
            #print dirnames
            #print filenames

            for filename in fnmatch.filter(filenames, self.rlogpattern):
                radiomatches.append(os.path.join(root, filename))

        kernelmatches = list()
        for root, dirnames, filenames in os.walk(dirname):
            #print root
            #print dirnames
            #print filenames
            for filename in fnmatch.filter(filenames, self.klogpattern):
                kernelmatches.append(os.path.join(root, filename))

        for mindex, mname in enumerate(mainmatches):
            #get pattern
            mpattern = "0-main-(.*).log"
            mcpattern = re.compile(mpattern)
            datematch = mcpattern.search(mname)
            if datematch:
                datepattern = datematch.group(1)
                onematch = dict()
                onematch['mainlog'] = mname

                self.logger.logger.info('date pattern is ' + datepattern)
                #try to do the loop to find the radio
                for rindex, rname in enumerate(radiomatches):
                    if datepattern in rname:
                        onematch['radiolog'] = rname
                        break
                #TODO: do the loop to find the kernel log

                matches.append(onematch)

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
        pdf.setup(pdf)
        svg.setup(svg)


    def setup_noderenderers(self):
        box.setup(box)
        actor.setup(actor)
        beginpoint.setup(beginpoint)
        circle.setup(circle)
        cloud.setup(cloud)
        diamond.setup(diamond)
        dots.setup(dots)

    def getPattern(self, taglist):
        '''
        used to get comma delimetered value config.ini
        :param taglist:
        :return: pattern
        '''
        if taglist :
            pattern = r''
            tagtype = type(taglist)
            if tagtype is list:
                for i,tag in enumerate(taglist):
                    pattern += str(tag) + '|'
                pattern = pattern[:len(pattern)-1]
            else:
                pattern += taglist
            return pattern
        else:
            self.logger.logger.error('tags is empty')
            return None

    def mergelistbykey(self, oldlist, keyname):
        #timestamp looks like 07-27 18:11:04.359
        #algorithm is sort month-day then sort by seconds
        newlist = sorted(oldlist, key=itemgetter(keyname))


        return newlist

    class dotdict(dict):
        """dot.notation access to dictionary attributes"""
        def __getattr__(self, attr):
            return self.get(attr)
        __setattr__= dict.__setitem__
        __delattr__= dict.__delitem__



if __name__ == '__main__':
    utils = utils()
    matches = utils.findlogs('./src')
    for index, match in enumerate(matches):
        for key,value in match.iteritems():
            print 'key is ' + key + ', value is ' + value
    a = list()
    a1 = dict()
    a2 = dict()
    a3 = dict()
    a1['timestamp'] = "07-27 18:11:04.359"
    a1['value'] = 'a1'
    a2['timestamp'] = "07-26 18:11:04.35"
    a2['value'] = 'a2'
    a3['timestamp'] = "07-28 18:11:04.35"
    a3['value'] = 'a3'
    a.append(a1)
    a.append(a2)
    a.append(a3)
    b = utils.mergelistbykey(a, 'timestamp')
    print 'before sort is '
    for index, element in enumerate(a):
        for key,value in element.iteritems():
            print 'key is ' + key + ', value is ' + value
    print 'after sort is '
    for index, element in enumerate(b):
        for key,value in element.iteritems():
            print 'key is ' + key + ', value is ' + value

