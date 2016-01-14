#-*- coding=utf-8 -*-
'''
@description: 核心购票新接口测试用例基类。
@author: miliang<miliang@baidu.com>

'''
import sys
import copy
import urllib
import urllib2
import json
import hashlib
import time
import MySQLdb
import redis
from base import Ticket_Base
from settings import SERVER,REDIS_CONF,MYSQL,ONLINE_SIGN_KEY

class Online_Ticket_Util(Ticket_Base):
    def __init__(self):
        super(Ticket_Base,self).__init__()
        self.base_url = 'http://dianying.baidu.com/ticket/'
        self.sign_key = ONLINE_SIGN_KEY
        self.redis = redis.Redis(REDIS_CONF['HOST'],REDIS_CONF['PORT'],REDIS_CONF['DB'])

                
if __name__ == '__main__':
    util = Online_Ticket_Util()
    print util.lockSeat(sys.argv[1])
    #print util.lockSeat('wangpiao',seq_no='17345994',third_id='1095',seat_index=1,mode=1)
    #print util.lockAllSeat('newvista','0000000000004878','dadi0201')
