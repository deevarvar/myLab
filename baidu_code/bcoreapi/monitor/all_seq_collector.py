#-*- coding=utf-8 -*-
'''
@description: 影讯信息获取类。
@author: miliang<miliang@baidu.com>

'''
import sys
sys.path.append('../')
import copy
import urllib
import urllib2
import json
import hashlib
import time
import MySQLdb
import redis
import socket
from monitor.settings import MODE,MYSQL,SEQ_INFO_FILE,REDIS_CONF,PARTNERS
from info.base import Info_Base
from ticket.base import Ticket_Base
from info.online_info_util import Online_Info_Util
from ticket.online_ticket_util import Online_Ticket_Util

class All_Seq_Collector(object):
    def __init__(self,third_from):
        self.output_file_name = SEQ_INFO_FILE
	self.third_from = third_from
        try:
            self.redis = redis.Redis(REDIS_CONF['HOST'],REDIS_CONF['PORT'],REDIS_CONF['DB'])
        except:
            print 'Failed to connect to redis.'        

    def pre_execute(self):
        is_all_queues_empty = 1
        if self.redis.scard(REDIS_CONF['ALL_SEQ_SET']+'_'+self.third_from) != 0:
            is_all_queues_empty = 0
        if is_all_queues_empty == 1:
            self.execute()
        else:
            time.sleep(300)

    def execute(self):
        # 线下模式
        ticket_util = Ticket_Base()
        # 线上模式
        #ticket_util = Online_Ticket_Util()

        output_file = open(self.output_file_name,'w')
        # 1. 获取所有排期
        all_seqs = ticket_util.getAllSchedules(self.third_from)
        # 2. 将所有排期写入redis
        for seq in all_seqs:
            seq_string = '%s %s %s\n'%(seq['third_id'],seq['seq_no'],seq['seq_outbuy_time'])
            # 写入文件
            if MODE != 1:
                output_file.write(seq_string)
            # 写入redis,分合作方存储。
            else:
                self.redis.sadd(REDIS_CONF['ALL_SEQ_SET']+'_'+self.third_from,seq_string)
        


if __name__ == '__main__':
    test = All_Seq_Collector(sys.argv[1])
    while True:
        test.pre_execute()
