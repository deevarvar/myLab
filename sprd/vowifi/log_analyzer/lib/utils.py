#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com


import os
import sys
import re
import fnmatch
import errno
import subprocess
import blockdiag
import blockdiag.imagedraw
from blockdiag.noderenderer import box,actor,beginpoint,circle,cloud,diamond,dots

import blockdiag.plugins
from blockdiag.imagedraw import png,pdf,svg
import shutil
from easygui import *
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

            self.ylog = False

            #NOTE: logpatten is a list


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

        #UPDATED: for ylog, add android, kernel dir to run analyzer.py
        #
        matches = list()

        mainmatches = list()

        #if analyze.py exist, so call it.
        for root, dirnames, filenames in os.walk(dirname):
            for i, dname in enumerate(dirnames):
                if 'android' == dname or 'kernel' == dname:
                    analyerfile = root + '/' + dname + '/' + 'analyzer.py'
                    if(os.path.exists(analyerfile)):
                        self.ylog = True
                        subprocess.call(analyerfile, shell=True)

        if self.ylog:
            self.mlogpattern = self.config['files']['ylog']
            self.rlogpattern = self.config['files']['radioylog']
            self.klogpattern = self.config['files']['kernellog']
        else:
            self.mlogpattern = self.config['files']['log']
            self.rlogpattern = self.config['files']['radiolog']
            self.klogpattern = self.config['files']['kernellog']
        self.clogpattern = self.config['files']['crashlog']

        for root, dirnames, filenames in os.walk(dirname):
            #print root
            #print dirnames
            #print filenames

            for filename in fnmatch.filter(filenames, self.mlogpattern):
                onematch = dict()
                onematch['log'] = os.path.realpath(os.path.join(root, filename))
                onematch['dir'] = root
                #delete the dir tree existing
                outputdir = root + '/' + filename.split('.')[0]
                if os.path.isdir(outputdir):
                    try:
                        shutil.rmtree(outputdir)
                    except OSError as e:
                        errorstr = "Error Happened!\n"
                        errorstr += str(e.strerror) + '\n' + str(e.filename)
                        msgbox(errorstr)
                        return -1
                mainmatches.append(onematch)

        #dirty hacks , what if ylog is disabled....
        if len(mainmatches) == 0:
            print 'enter'
            self.mlogpattern = self.config['files']['log']
            self.rlogpattern = self.config['files']['radiolog']
            for root, dirnames, filenames in os.walk(dirname):
            #print root
            #print dirnames
            #print filenames

                for filename in fnmatch.filter(filenames, self.mlogpattern):
                    onematch = dict()
                    onematch['log'] = os.path.realpath(os.path.join(root, filename))
                    onematch['dir'] = root
                    #delete the dir tree existing
                    outputdir = root + '/' + filename.split('.')[0]
                    if os.path.isdir(outputdir):
                        shutil.rmtree(outputdir)
                    mainmatches.append(onematch)


        '''
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
        '''
        #use this logic: radio is the same dir, kernel is in the ../kernel/, so just search

        for mindex, mname in enumerate(mainmatches):
            mainlog = mname['log']
            radiodir = mname['dir']
            kerneldir = mname['dir'] + '/../kernel/'
            onematch = dict()
            onematch['mainlog'] = mainlog
            onematch['radiolog'] = ''
            onematch['kernellog'] = ''
            for rfile in os.listdir(radiodir):
                if os.path.isfile(os.path.join(radiodir, rfile)):
                    if fnmatch.fnmatch(rfile, self.rlogpattern):
                        onematch['radiolog'] = os.path.realpath(os.path.join(radiodir, rfile))
            if os.path.exists(kerneldir):
                for kfile in os.listdir(kerneldir):
                    if os.path.isfile(os.path.join(kerneldir, kfile)):
                        if fnmatch.fnmatch(kfile, self.klogpattern):
                            onematch['kernellog'] = os.path.realpath(os.path.join(kerneldir, kfile))

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
    def humansize(self,nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    def findfields(self, line):
        #for android log before android o
        #08-23 21:47:17.415  1118  1118 D LEMON   : 21:47:17.415
        #after android o
        #00D347 08-23 19:57:51.585  1205  1254 D LEMON
        #but sometimes, still ..., so the log team sucks
        fields = line.split()
        datepattern= "\d\d-\d\d"
        dpattern = re.compile(datepattern)
        first = fields[0]
        match = dpattern.match(first)
        fruit = dict()
        fruit['day'] = ""
        fruit['time'] = ""
        fruit['pid'] = ""
        if match:
            fruit['day'] = fields[0]
            fruit['time'] = fields[1]
            fruit['pid'] = fields[2]
        else:
            fruit['day'] = fields[1]
            fruit['time'] = fields[2]
            fruit['pid'] = fields[3]
        return fruit

    class dotdict(dict):
        """dot.notation access to dictionary attributes"""
        def __getattr__(self, attr):
            return self.get(attr)
        __setattr__= dict.__setitem__
        __delattr__= dict.__delitem__



if __name__ == '__main__':
    utils = utils()
    line1 = "08-23 21:47:17.415  1118  1118 D LEMON   : 21:47:17.415"
    line2 = "00D347 08-23 19:57:51.585  1205  1254 D LEMON"
    fruit = utils.findfields(line1)
    print fruit
    fruit = utils.findfields(line2)
    print fruit
    matches = utils.findlogs('./src/dtac_video_mo/')
    for index, match in enumerate(matches):
        for key,value in match.iteritems():
            print 'key is ' + key + ', value is ' + value

'''
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
'''
