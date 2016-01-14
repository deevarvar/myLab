#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import sys
import os
import pdb
PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../")
sys.path.append(PROJECT_PATH + 'lib')
import settings
import configobj
from configobj import ConfigObj

mockdir = PROJECT_PATH+'mockserver'
sys.path.append(mockdir)

import logging.config
import copy



class RspHelper(object):
    CORRECT = 2
    ONGOING = 1
    WRONG = 0
    def __init__(self, third, configfile):
        try:
            config = ConfigObj(configfile)
            #TODO: add conf check later use configobj
            self.conf = config
            self.third = third
            #init the logging setting
            logging.config.dictConfig(settings.LOGGING)
            self.logger = logging.getLogger('mockserver')
        except configobj.ConfigObjError as e:
            print e
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print 'exception is %s'% str(e)
            #pdb.post_mortem(sys.exc_info()[2])

    def getdelaytime(self, api):
        delay = self.conf[self.third]['delay_time'][api]['delay']
        rate = self.conf[self.third]['delay_time'][api]['rate']
        self.logger.info(self.third + ' delay is ' +  str(delay) + ', rate is ' + str(rate))
        #1. handle all rate as list
        delay_dict = []
        rate_dict = []
        if isinstance(delay, str):
            delay_dict.append(delay)
        else:
            delay_dict = copy.deepcopy(delay)

        if isinstance(rate, str):
            rate_dict.append(rate)
        else:
            rate_base = 0
            for r in rate:
                rate_base = rate_base + int(r)
                rate_dict.append(rate_base)

        waterlevel = random.randint(0, 100)
        self.logger.info(self.third + ' waterlevel is ' + str(waterlevel) +' delay_dict is ' + str(delay_dict) + ', rate_dict is ' + str(rate_dict))

        #2. compare with the waterlevel
        for index, val in enumerate(rate_dict):
            #if rate conf is not right, default rate is 100
            if not val:
                val = '100'
            if waterlevel <= int(val):
                #if delay conf is not right , default delay is 0
                if not delay_dict[index]:
                   self.logger.error('conf for '+self.third + ' delay time index ' +  str(index) + 'is missing.')
                   delay_time = '0'
                else:
                    delay_time = delay_dict[index]
                self.logger.info(self.third + ' delay time for ' + api + ' is ' + delay_time)
                return delay_time
        #if conf is not correct
        self.logger.error('conf for '+ self.third + ' delay rate is not set correctly.')
        return str(random.randint(0,2))

    def getrsptype(self, api):
        waterlevel = random.randint(0,100)
        rate_dict = []
        #add simple config check
        correct_rate = self.conf[self.third]['rsp_rate'][api]['correct']
        if not correct_rate:
            correct_rate = '100'
        correct_obj = dict()
        correct_obj['rate'] = correct_rate
        correct_obj['type'] = self.CORRECT
        rate_dict.append(correct_obj)

        wrong_rate = self.conf[self.third]['rsp_rate'][api]['wrong']
        #add some corner case handling
        leftrate = str((100 - int(correct_rate))/2)

        if not wrong_rate:
            wrong_rate = leftrate
        wrong_obj = dict()
        wrong_obj['rate'] = str(int(correct_rate) + int(wrong_rate))
        wrong_obj['type'] = self.WRONG
        rate_dict.append(wrong_obj)

        ongoing_rate = self.conf[self.third]['rsp_rate'][api]['ongoing']
        if not ongoing_rate:
            ongoing_rate = leftrate
        ongoing_obj = dict()
        ongoing_obj['rate'] = str(int(ongoing_rate) + int(wrong_rate)+int(correct_rate))
        ongoing_obj['type'] = self.ONGOING
        rate_dict.append(ongoing_obj)

        self.logger.info(self.third+' waterlevel is ' + str(waterlevel)+' correct/wrong/ongoing rate is '+ str(rate_dict))

        for index,val in enumerate(rate_dict):
            if waterlevel <= int(val['rate']):
                self.logger.info(self.third+' rsp type is '+ str(val['type']))
                return val['type']
        self.logger.error('conf for '+ self.third + ' rsp rate is not set correctly.')
        return self.CORRECT


if __name__ == '__main__':
    helper = RspHelper('cmts', PROJECT_PATH + 'conf/cmts.conf')
    helper.logger.info(helper.conf)
