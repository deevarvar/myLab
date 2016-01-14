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
from info.online_info_util import Online_Info_Util

class Seq_Info_Collector(object):
    def __init__(self):
        self.output_file_name = SEQ_INFO_FILE
        try:
            self.redis = redis.Redis(REDIS_CONF['HOST'],REDIS_CONF['PORT'],REDIS_CONF['DB'])
        except:
            print 'Failed to connect to redis.'
        
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.conn = '/home/map/miliang/new_api_auto_test/monitor/conn'
        try:
            self.sock.connect(self.conn)
        except:
            print 'Failed to connect to socket server(mysql updater).'



    def pre_execute(self):
        is_all_queues_empty = 1
        for partner in PARTNERS:
            if self.redis.llen(REDIS_CONF['SEQ_DATA_Q']+'_'+partner) != 0:
                is_all_queues_empty = 0
        if is_all_queues_empty == 1:
            self.execute()
        else:
            time.sleep(300)

    def execute(self):
        # 线下模式
        info_util = Info_Base()
        # 线上模式
        #info_util = Online_Info_Util()

        output_file = open(self.output_file_name,'w')
        # 1. 获取所有影院列表
        cinema_index_api = info_util.req_url + 'allcinemas'
        params = {"req_from":"movie_c"}
        try:
            cinema_index = info_util.doRequest(cinema_index_api,params)
        except:
            print "Failed to get cinema index!!!"
        cinema_list = []
        for cinema in cinema_index['data']:
            #print repr(cinema['name'])
            cinema_list.append((cinema['cinema_id'],cinema['name']))
        # 2. 获取各影院合作方、third_id、排期信息
        schedule_api = info_util.req_url + 'schedule'
        params = {}
        for cinema in cinema_list:
            # 如果正在更新数据库，等待。
            
            while True:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                conn = '/home/map/miliang/new_api_auto_test/monitor/conn'
                try:
                    sock.connect(conn)
                except:
                    print 'Failed to connect to socket server(mysql updater).'
                sock.send('hello,server') # whatever the message is...
                is_update_mysql = sock.recv(1024)
                if is_update_mysql == '0':
                    sock.close()
                    break
                else:
                    print "Mysql updating,wait..."
                    time.sleep(30)
                    continue
            

            params['cinema_id'] = cinema[0]
            try:
                schedule = info_util.doRequest(schedule_api,params)
            except:
                print "Failed to get schedule!!! Cinema_id : %s." % cinema_id
            for date in schedule['time_table']:
                for seq in schedule['time_table'][date]:
                    if not seq['time'] or not seq['date']:
                        continue
                    seq_datetime = seq['date'] + ' ' + seq['time']
                    try:
                        seq_outbuy_time = time.mktime(time.strptime(seq_datetime, '%Y-%m-%d %H:%M'))
                    except:
                        seq_outbuy_time = time.mktime(time.strptime(seq_datetime, '%Y-%m-%d %H:%M:%S'))
                    time_threshold = time.time()+2*60*60
                    if seq_outbuy_time < time_threshold:
                        continue

                    #for prior in range(len(seq['src_info'])):
                    for prior in range(1):
                        third_from = seq['src_info'][prior]['src']
                        third_id = seq['src_info'][prior]['third_cinema_id']
                        seq_no = seq['src_info'][prior]['seq_no']
                        cinema_id = cinema[0]
                        cinema_name = cinema[1]
                        #print repr(cinema[1])
                        seq_string = '%s %s %s %s %s %r %s\n'%(third_from,third_id,seq_no,prior,cinema_id,cinema_name,seq_outbuy_time)
                        # 写入文件
                        if MODE != 1:
                            output_file.write(seq_string)
                        # 写入redis,分合作方存储。
                        else:
                            self.redis.lpush(REDIS_CONF['SEQ_DATA_Q']+'_'+third_from,seq_string)
        


if __name__ == '__main__':
    test = Seq_Info_Collector()
    while True:
        test.execute()
