#-*- coding=utf-8 -*-
'''
@description: 锁座功能监控。
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
import thread
import socket
from monitor.settings import MYSQL,SEQ_INFO_FILE,PARTNERS,REDIS_CONF,MODE,PARTNERS_THREAD_NUM
from ticket.base import Ticket_Base
from ticket.online_ticket_util import Online_Ticket_Util

#socket.setdefaulttimeout(2)

class Lock_Seat_Press(object):
    def __init__(self,third_from=None):
        self.seq_info_file_name = SEQ_INFO_FILE
        # 以本地文件方式获得场次信息
        self.seq_info_file = open(self.seq_info_file_name,'r')
        # 以redis方式获得场次信息
        self.third_from = third_from
        self.redis = redis.Redis(REDIS_CONF['HOST'],REDIS_CONF['PORT'],REDIS_CONF['DB'])

    def execute(self):
        # 线下模式
        #ticket_util = Ticket_Base()
        # 线上模式
        ticket_util = Online_Ticket_Util() 

        # 设置超时
        ticket_util.setTimeout(10)
		
        output_file = open('urls.txt','w')

        while True:
            '''
            # 检查是否正在更新数据库，若是，需要等待
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

            '''
            # redis模式
            if MODE == 1:
                if self.redis.scard(REDIS_CONF['ALL_SEQ_SET']+'_'+self.third_from) == 0:
                    print 'Seq queue empty for parterner: ' + self.third_from
                    break
                seq_string = self.redis.spop(REDIS_CONF['ALL_SEQ_SET']+'_'+self.third_from)
            
            # 文件模式
            else:
                seq_string = self.seq_info_file.readline()
                if not seq_string:
                    break

            # 开始解析场次信息
            seq_info = seq_string.strip('\n').split(' ')
            third_from = self.third_from
            third_id = seq_info[0]
            seq_no = seq_info[1]
            seq_outbuy_time = int(seq_info[2].split('.')[0])

            if not third_from or not third_id or not seq_no:
                continue
            if self.third_from and self.third_from != third_from:
                continue
            time_threshold = int(time.time())+2*60*60

            if seq_outbuy_time < time_threshold:
                continue
            # 调用座位图接口
            params = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id}
            base_url = '/ticket/seat/get'
            url = ticket_util.genUrl(base_url,params)
            output_file.write(url+'\n')

            # 异常处理
            #self.dealException(exception_no,seat_url,xpt_string,cinema_id)

    def dealException(self,e_no,seat_url,xpt_string,cinema_id):
        if e_no == 0: # 正常
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        elif e_no == 1: # 满场
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        elif e_no == 2: # 座位图获取失败
            print '[Fail to get seat info] ' + seat_url
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'1')
            self.redis.lpush(REDIS_CONF['CINEMA_XPT_Q']+'_'+cinema_id,xpt_string)
            #self.redis.lpush(REDIS_CONF['SEQ_XPT_Q']['SEAT_INFO'][0]+'_'+self.third_from,xpt_string)
        elif e_no == 3: # 锁座失败
            print '[Fail to lock seat or timeout] ' + seat_url
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'1')
            self.redis.lpush(REDIS_CONF['CINEMA_XPT_Q']+'_'+cinema_id,xpt_string)
            #self.redis.lpush(REDIS_CONF['SEQ_XPT_Q']['LOCK_SEAT'][0]+'_'+self.third_from,xpt_string)
        elif e_no == 4: # 锁座成功而返回错误码
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        elif e_no == 5: # 锁座场次信息为空
            print '[Lock result without seq_no.]' + seat_url
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        else:
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')      
        
def run(third_from):
    case = Lock_Seat_Press(third_from)
    case.execute()

if __name__ == '__main__':
   
    '''
    for partner in PARTNERS:
        try:
            for i in range(PARTNERS_THREAD_NUM[partner]):
                thread.start_new_thread( run, (partner, ) )
        except:
            print "Error: unable to start thread when dealing with %s." % partner
    while 1:
        pass
    
    run('cmts')
    '''
    
    third_from = sys.argv[1]
    run(sys.argv[1])
    '''
    try:
        for i in range(50):
            thread.start_new_thread( run, (third_from, ) )
    except:
        print "Error: unable to start thread."
    while 1:
        pass 
    '''
