#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import re

#logging.getLogger("urllib3").setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
#init the logging
basiclog = logging.getLogger()
basiclog.setLevel(logging.DEBUG)
debugHandler = logging.FileHandler('./test.log', mode='w')
debugHandler.setLevel(logging.DEBUG)
debugHandler.setFormatter(formatter)
basiclog.addHandler(debugHandler)
info = logging.StreamHandler(sys.stdout)
info.setLevel(logging.DEBUG)
info.setFormatter(formatter)
basiclog.addHandler(info)

basiclog.info('hello, info!')
basiclog.warn('hello, warn!')
basiclog.error('hello, error!')
basiclog.critical('hello, critical!')

line = '0396:2015-04-02 19:03:51,527 - normal - DEBUG - CheckAction.py - getTimetable - 119 - movie link is /dianying/plan?seq_no=18180499&cinema_id=2161&third_from=wangpiao'
third_from_pattern = '.*third_from=(?P<third_from>(.*))'
m = re.search(third_from_pattern, line)
if m is not None:
    print(m.group('third_from'))

teststring=['newvista' , 'lumiai']
target = 'newvista'
if target in teststring:
    print 'in!'
else:
    print 'not in!'


for i in range(0,0):
    print i