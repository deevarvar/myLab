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
from monitor.settings import SERVER,MYSQL,SEQ_INFO_FILE
from ticket.base import Ticket_Base

class Seat_Info_Monitor(object):
    def __init__(self):
        self.seq_info_file_name = SEQ_INFO_FILE

    def execute(self):
        ticket_util = Ticket_Base()
        seq_info_file = open(self.seq_info_file_name,'r')
        while True:
            line = seq_info_file.readline()
            if not line:
                break
            seq_info = line.strip('\n').split(' ')
            third_from = seq_info[0]
            third_id = seq_info[1]
            seq_no = seq_info[2]
            prior = seq_info[3]
            if not third_from or not third_id or not seq_no:
                continue
            # 获取座位图
            seat_info_api = ticket_util.req_url + 'seat/get'
            params = {}
            params['third_from'] = third_from
            params['third_id'] = third_id
            params['seq_no'] = seq_no
            try:
                seat_info = ticket_util.doRequest(seat_info_api,params)
            except:
                print "[Api Error]Get seat info failed !!! third_from: %s, third_id: %s, seq_no: %s." % (third_from,third_id,seq_no)
            if seat_info['errorMsg'] != 'Success' or not seat_info['data']:
                print "[Response Error]Get seat info failed !!! third_from: %s, third_id: %s, seq_no: %s." % (third_from,third_id,seq_no)


if __name__ == '__main__':
    test = Seat_Info_Monitor()
    test.execute()
