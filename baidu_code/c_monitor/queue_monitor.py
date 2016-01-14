#!/usr/bin/env python
#-*- coding=utf-8 -*-
#author: yezhihua@baidu.com

import os
import logging
import sys
import requests
from pyquery import PyQuery

class queue_monitor():
    MQURL="http://m1-wg-mop00.m1.baidu.com:8161/admin/queues.jsp"
    MQUSER="admin"
    MQPASSWD="admin"
    MQHTML="./mq.html"
    NAME_INDEX=0
    VALUE_TD_INDEX=1

    '''
        patttern is used to match the page's tr
        key is the resutl key
        level is the threshhold if the alarm will be triggered.
        index is the tr index in the page
    '''
    MATCH_RULE = [
        {
            "pattern" : "schedulequeue", #online_schedulequeue
            "fullname" : "online_schedulequeue",
            "key" : "schedulenum",
            "level" : 50,
            "index" : 0
        },
        {
            "pattern" : "adjust", #queue.movie.budget.adjust
            "fullname" : "queue.movie.budget.adjust",
            "key" : "adjustnum",
            "level" : 100,
            "index" : 1
        },
        {
            "pattern" : "record", #queue.movie.budget.record
            "fullname" : "queue.movie.budget.record",
            "key" : "recordnum",
            "level" : 100,
            "index" : 2
        }
    ]

    def __init__(self):
        self.level = logging.INFO
        self.log = self.setLogOutput()

    def setLogOutput(self):
        debugfile =  './debug_cmonitor.log'
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
        #init the logging
        basiclog = logging.getLogger('normal')
        basiclog.setLevel(logging.DEBUG)
        debugHandler = logging.FileHandler(debugfile, mode='w')
        debugHandler.setLevel(logging.DEBUG)
        debugHandler.setFormatter(formatter)
        basiclog.addHandler(debugHandler)
        info = logging.StreamHandler(sys.stdout)
        info.setLevel(self.level)
        info.setFormatter(formatter)
        basiclog.addHandler(info)
        return basiclog


    def fixIndex(self,name, index):
        #in case the name order will be changed.
        for item in self.MATCH_RULE:
            if item['pattern'] in name:
                self.log.info('pattern ' + item['pattern'] + ' is in '+name + ', index is '+str(index))
                item['index'] = index
                break

    def getValue(self,jquery):
        result = {
            "schedulequeue": {},
            "adjust": {},
            "record": {}
        }
        for item in self.MATCH_RULE:
            tr_index = item['index']
            valueselector = '#queues tr:eq('+ str(tr_index) +') td:eq('+ str(self.VALUE_TD_INDEX) +')'
            num = jquery(valueselector).html()
            result[item['pattern']] = {
                "num": str(num),
                "level": item['level'],
                "name" : item['fullname']
            }
        self.log.info('result is '+ str(result))
        return result

    def getPage(self):
        result = {}
        try:
            rsp =  requests.get(self.MQURL, auth=(self.MQUSER, self.MQPASSWD))
            with open(self.MQHTML, 'w+') as mqfile:
                mqfile.write(rsp.content)
            jquery = PyQuery(filename=self.MQHTML)

            trlen = jquery('#queues tr').length
            #skip one row
            for index in range(0,trlen-1):
                nameselector = '#queues tr:eq('+ str(index) +') td:eq('+ str(self.NAME_INDEX) +') a'
                pend = jquery(nameselector)
                name=pend.html().strip()
                self.log.info('index is '+str(index) + ' ' + name)
                self.fixIndex(name, index)

            result = self.getValue(jquery)
            return result
        except requests.exceptions.RequestException as e:
            self.log.error(e)
        return result
    def run(self):
        print self.getPage()


if __name__ == '__main__':
    queue_monitor().run()