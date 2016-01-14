#-*- coding=utf-8 -*-
'''
@description: 旧支付回调接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
import os
import time
import copy
import urllib
import urllib2
import json
import hashlib
import MySQLdb
from settings import SERVER,MYSQL,ODP_MOVIE_PATH,PAY_NOTICE_SIGN_KEY
from base import Ticket_Base
from old_lock_seat import Ticket_Old_Lock_Seat

class Ticket_Old_Pay_Notice(Ticket_Base):
    def __init__(self,third_from,third_order_id=None,cinema_index=1,num=1,seq_no=None,third_id=None,mode=0,device='pc'):
        super(Ticket_Old_Pay_Notice,self).__init__()
        self.req_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/paynotice/' + third_from + '/' + device
        # 若没有指定third_order_id，需要自行执行锁座并获取third_order_id
        if not third_order_id:
            lockseat = Ticket_Old_Lock_Seat(third_from=third_from,cinema_index=cinema_index,num=num)
            try:
                lockseat.execute()
            except:
                assert 0>1
            third_order_id = lockseat.third_order_id
        
        print 'third_order_id: ' + third_order_id
        self.req_dict = {}
        self.req_dict['orderId'] = third_from + third_order_id
        self.req_dict['status'] = 'PAY_SUCCESS'
        #self.req_dict['txNo'] = 1234567
        self.req_dict['paidAmount'] = 1
        self.req_dict['totalAmount'] = 1
        self.req_dict['reduction'] = 0
        self.req_dict['requestId'] = 1234567
        self.req_dict['sign'] = self.GenPayNoticeSign(self.req_dict)
        
        self.third_from = third_from
        self.third_order_id = third_order_id

    def execute(self):
        self.page_dict = self.doPostRequest(self.req_url,self.req_dict)
        self.doAssert()
    '''   
    def execute(self):
        # 若接口返回的buy_status=3,引入重试机制查询出票最终状态
        retry_max = 5
        retry = 0
        while True:
            if retry == retry_max:
                break
            try:
                self.page_dict = self.doRequest(self.req_url,self.req_dict)
                print ":::::page_dict::::::"
                print self.page_dict
            except:
                retry += 1
                time.sleep(1.5)
                continue
            if not self.page_dict or not self.page_dict.has_key('buy_status'):
                retry += 1
                time.sleep(1.5)
                continue
            if int(self.page_dict['buy_status']) != 3:
                break
            retry += 1
            time.sleep(1.5)

        self.doAssert()
    '''
    def doAssert(self):
        # 同步第三方订单
        time.sleep(2)
        cmd = 'cd %s&&%s/php/bin/php %s/app/ticket/script/sync%sOrders.php' % (ODP_MOVIE_PATH,ODP_MOVIE_PATH,ODP_MOVIE_PATH,self.third_from[0].upper()+self.third_from[1:])
        print ':::: cmd ::::' + cmd
        os.system(cmd)
        # 验证数据库中该订单是否有出票码信息
        mysql = MySQLdb.connect(host=MYSQL['HOST'],port=MYSQL['PORT'],db=MYSQL['DB'],user=MYSQL['USER'],passwd=MYSQL['PASSWD'],charset='utf8')
        cursor = mysql.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from t_movie_order where third_order_id='%s' and third_from='%s'" % (self.third_order_id,self.third_from)
        print ':::: sql ::::' + sql
        cursor.execute(sql)
        order_info = cursor.fetchall()
        print order_info
        assert len(order_info) != 0
        print order_info[0]['sms_ticket_code']
        assert order_info[0]['sms_ticket_code']
        
    def GenPayNoticeSign(self,params_origin):
        params = copy.deepcopy(params_origin)
        params = sorted(params.iteritems(), key=lambda d:d[0])
        print params
        sign_string = ""
        for param in params:
            print param
            sign_string += '%s=%s&' % (param[0],param[1])
        sign_string += 'key=' + PAY_NOTICE_SIGN_KEY
        print "Sign string: " + sign_string
        sign = hashlib.new("md5", sign_string).hexdigest()
        return sign        

if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Old_Pay_Notice(sys.argv[1])
    elif len(sys.argv) == 3:
        case = Ticket_Old_Pay_Notice(sys.argv[1],third_order_id=sys.argv[2])
    elif len(sys.argv) == 4:
        #case = Ticket_Old_Pay_Notice(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3],mode=1)
        case = Ticket_Old_Pay_Notice(sys.argv[1],num=int(sys.argv[2]),cinema_index=int(sys.argv[3]))
    else:
        case = Ticket_Old_Pay_Notice('lanhai')

    case.execute()
