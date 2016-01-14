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

class Lock_Seat_Monitor(object):
    def __init__(self,third_from=None):
        self.seq_info_file_name = SEQ_INFO_FILE
        # 以本地文件方式获得场次信息
        self.seq_info_file = open(self.seq_info_file_name,'r')
        # 以redis方式获得场次信息
        self.third_from = third_from
        self.redis = redis.Redis(REDIS_CONF['HOST'],REDIS_CONF['PORT'],REDIS_CONF['DB'])

    def execute(self):
        # 线下模式
        ticket_util = Ticket_Base()
        # 线上模式
        #ticket_util = Online_Ticket_Util() 

        while True:
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

            # redis模式
            if MODE == 1:
                if self.redis.llen(REDIS_CONF['SEQ_DATA_Q']+'_'+self.third_from) == 0:
                    #print 'Seq queue empty for parterner: ' + self.third_from
                    #break
                    time.sleep(5)
                    continue
                seq_string = self.redis.rpop(REDIS_CONF['SEQ_DATA_Q']+'_'+self.third_from)
            
            # 文件模式
            else:
                seq_string = self.seq_info_file.readline()
                if not seq_string:
                    break

            # 开始解析场次信息
            seq_info = seq_string.strip('\n').split(' ')
            third_from = seq_info[0]
            third_id = seq_info[1]
            seq_no = seq_info[2]
            prior = seq_info[3]
            cinema_id = seq_info[4]
            cinema_name = seq_info[5] # 这里的cinema_name是repr后的结果，不可能有空格
            # 还真有带有空格的影院名- -
            try:
                seq_outbuy_time = int(seq_info[6].split('.')[0])
            except:
                cinema_name = seq_info[5] + seq_info[6]
                seq_outbuy_time = int(seq_info[7].split('.')[0])

            if not third_from or not third_id or not seq_no:
                continue
            if self.third_from and self.third_from != third_from:
                continue
            time_threshold = int(time.time())+2*60*60

            if seq_outbuy_time < time_threshold:
                continue
            # 由于延迟问题，每次锁座检验都检查之前锁过的所有座位
            check_seats = []

            # 锁座
            seat_url = 'http://map.baidu.com/detail?qt=movie&act=select&from=pc&seq_no=%s&cinema_id=%s&third_from=%s&sfrom=map' % (seq_no,third_id,third_from)
            #print seat_url
            # 异常号：0为正常，1为满座，2为座位图获取失败，3为锁座失败，4为锁座成功而返回错误码，5为锁座场次信息为空
            exception_no = 0
            for retry in range(5):
                lock_result = ticket_util.lockSeat(third_from,seq_no=seq_no,third_id=third_id,seat_index=1+retry*10,mode=1)
                # 异常影院信息，包括影院名，合作方，选座url
                xpt_string = '%s %s %s %s' % (cinema_name,third_from,seat_url,time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime(time.time())))
                
                #print 'lock e no:' + str(lock_result['error_no'])
                if lock_result['error_no'] == 2001: # 已无更多符合条件的座位
                    break
                
                if lock_result['error_no'] == 1002: # 满场，无需处理
                    exception_no = 1
                    break

                if lock_result['error_no'] == 1001: # 座位图获取失败
                    exception_no = 2
                    continue
                    #print '[Fail to get seat info] ' + seat_url
                    #self.redis.lpush(REDIS_CONF['SEQ_XPT_Q']['SEAT_INFO'][0]+'_'+third_from,xpt_string)

                if not lock_result.has_key('third_order_id') or not lock_result['third_order_id']: # 锁座失败或超时
                # 检查是否锁座成功
                    if lock_result.has_key('seq_no'):
                        check_seats.append(lock_result['seat_no'])
                        # 由于延迟问题，每次锁座检验都检查之前锁过的所有座位
                        for seat_to_check in check_seats:
                            lock_check = ticket_util.getSeatStatus(third_from,seq_no=lock_result['seq_no'],third_id=lock_result['third_id'],seat_no=seat_to_check)
                            if lock_check['lock_status'] == 1: 
                                exception_no = 3
                                #print lock_result['seat_no']
                            elif lock_check['lock_status'] == 2:
                                exception_no = 4
                                break
                            else :
                                exception_no = 99
                                break
                        if exception_no != 3:
                            break
                        # 这里可以写每次重试的延迟
                        #time.sleep(10)
                    else:
                        exception_no = 5
                        continue

                else:
                    exception_no = 0
                    break
            # 异常处理
            self.dealException(exception_no,seat_url,xpt_string,cinema_id)

    def dealException(self,e_no,seat_url,xpt_string,cinema_id):
        #print e_no
        if e_no == 0: # 正常
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        elif e_no == 1: # 满场
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        elif e_no == 2: # 座位图获取失败
            #print '[Fail to get seat info] ' + seat_url
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'1')
            self.redis.lpush(REDIS_CONF['CINEMA_XPT_Q']+'_'+cinema_id,xpt_string)
            #self.redis.lpush(REDIS_CONF['SEQ_XPT_Q']['SEAT_INFO'][0]+'_'+self.third_from,xpt_string)
        elif e_no == 3: # 锁座失败
            #print '[Fail to lock seat or timeout] ' + seat_url
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'1')
            self.redis.lpush(REDIS_CONF['CINEMA_XPT_Q']+'_'+cinema_id,xpt_string)
            #self.redis.lpush(REDIS_CONF['SEQ_XPT_Q']['LOCK_SEAT'][0]+'_'+self.third_from,xpt_string)
        elif e_no == 4: # 锁座成功而返回错误码
            print '[Lock succeeded but return error]' + seat_url
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        elif e_no == 5: # 锁座场次信息为空
            #print '[Lock result without seq_no.]' + seat_url
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')
        else:
            self.redis.lpush(REDIS_CONF['CINEMA_SEQ_Q']+'_'+cinema_id,'0')      
        
def run(third_from):
    case = Lock_Seat_Monitor(third_from)
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
    try:
        for i in range(10):
            thread.start_new_thread( run, (third_from, ) )
    except:
        print "Error: unable to start thread."
    while 1:
        pass 
