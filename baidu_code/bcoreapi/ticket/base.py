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
import random
import redis
import socket
from settings import SERVER,REDIS_CONF,MYSQL,SIGN_KEY, ODP_PAL_SERVER

import ticketlog
import logging.config
logging.config.dictConfig(ticketlog.LOGGING)
logger = logging.getLogger('ticket')

class Ticket_Base(object):
    def __init__(self):
        self.req_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/'
        self.base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/'
        #self.base_url = 'http://dianying.baidu.com/ticket/'
        self.sign_key = SIGN_KEY
        self.req_dict = {}
        self.page_dict = {}
        self.redis = redis.Redis(REDIS_CONF['HOST'],REDIS_CONF['PORT'],REDIS_CONF['DB'])


    def doAssert(self):
        pass

    def execute(self):
        self.page_dict = self.doRequest(self.req_url,self.req_dict)
        self.doAssert()

    def genUrl(self,base_url,params):
        sign = self.signGenerate(params)
        params['sign'] = sign
        query_string = urllib.urlencode(params)
        url = base_url + '?' + query_string
        return url

    def doRequest(self,base_url,params):
        sign = self.signGenerate(params)
        params['sign'] = sign
        query_string = urllib.urlencode(params)
        url = base_url + '?' + query_string
        logger.debug('::::Request url:::: ' + url)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }

        req = urllib2.Request(url,'',headers)
        # 超时检验
        try:
            response = urllib2.urlopen(req)
        except socket.timeout:
            logger.error('socket timeout')
            result = {"erroring" : 2}
            return result

        the_page = response.read()
        try:
            #print json.loads(the_page)
            return json.loads(the_page)
        except:
            logger.error('json decode error ' + the_page);
            result = {"erroring":1}
            return result

    def doPostRequest(self,base_url,params):

        query_string = urllib.urlencode(params)
        url = base_url + '?' + query_string
        #print '::::Request url:::: ' + url
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = urllib.urlencode(params)

        req = urllib2.Request(url,data,headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        logger.info(the_page)
        try:
            return json.loads(the_page)
        except:
            result = {"erroring":1}
            return result

    def signGenerate(self,params_origin):
        params = copy.deepcopy(params_origin)
        if params.has_key('log_id'):
            del params['log_id']
        if params.has_key('sign'):
            del params['sign']
        params = sorted(params.iteritems(), key=lambda d:d[0])
        sign = hashlib.new("md5", self.sign_key + urllib.urlencode(params)).hexdigest()
        sign = hashlib.new("md5", sign + self.sign_key).hexdigest()
        return sign

    def getSchedule(self,third_from,counter=1):
        '''
        @description: 场次查询
        @notes: 
        @input: 
            third_from : 合作方
            counter : 选择的满足条件的场次序号
        @output：
            result : 场次信息，包括合作方名称、场次号、影院第三方id。
        '''
        mysql = MySQLdb.connect(host=MYSQL["HOST"],port=MYSQL["PORT"],user=MYSQL["USER"],passwd=MYSQL["PASSWD"],db=MYSQL["DB"],charset="utf8")
        cursor = mysql.cursor()
        cmd = "select * from t_movie_cache_odp where third_from='%s' and data!='' order by id DESC limit 0,100" % (third_from)
        cursor.execute(cmd)
        for item in cursor.fetchall():
            third_id = item[1]
            # 去poi表查一下该影院有没有关联影院，没有则剔除
            logger.debug('try to get cinema_id is ' + str(third_id) +  ', third_from is ' + str(third_from))
            sql = "select cinemas_id  from t_movie_poi where third_from='%s' and third_id='%s' limit 0,1" % (third_from,third_id)
            cursor.execute(sql)
            poi_data = cursor.fetchall()
            #print poi_data[0][0]
            #logger.debug('cinema id is ' + str(poi_data[0][0]))
            if len(poi_data) == 0 or int(poi_data[0][0]) == 0:
                continue


            # 需要锁定某影院则需取消此段注释
            #if third_id != '32012101':
            #    continue
            try:
                time_table = json.loads(item[3])['time_table']
            except:
                continue
            refer_dict = {}
            if len(time_table) == 0 or type(time_table) == type(refer_dict):
                continue
            time_threshold = time.time()+2*60*60
            
            for day in range(len(time_table)):
                for seq in time_table[day]:
                    #logger.debug('time is '+seq['time'] + ', date is '+seq['date']);
                    if not seq['time'] or not seq['date']:
                        continue
                    seq_datetime = seq['date'] + ' ' + seq['time']
                    try:
                        seq_outbuy_time = time.mktime(time.strptime(seq_datetime, '%Y-%m-%d %H:%M'))
                    except:
                        seq_outbuy_time = time.mktime(time.strptime(seq_datetime, '%Y-%m-%d %H:%M:%S'))
                    if seq_outbuy_time < time_threshold:
                        continue
                    if not seq['src_info'][0]['seq_no']:
                        continue 
                    counter -= 1
                    if counter != 0:
                        continue
                    result = {}
                    result['seq_no'] = seq['src_info'][0]['seq_no']
                    result['origin_price'] = seq['origin_price']
                    result['third_from'] = third_from
                    result['third_id'] = third_id
                    result['movie_id'] = seq['src_info'][0]['movie_id']
                    if seq['src_info'][0].has_key('price'):
                        result['price'] = seq['src_info'][0]['price']
                    # fire锁座老接口需要的参数
                    if seq['src_info'][0].has_key('hall_id'):
                        result['hall_id'] = seq['src_info'][0]['hall_id']
                    if seq['src_info'][0].has_key('section_id'):
                        result['section_id'] = seq['src_info'][0]['section_id']
                    if seq['src_info'][0].has_key('show_seq_no'):
                        result['show_seq_no'] = seq['src_info'][0]['show_seq_no']
                    #print seq
                    return result

    def getSeat(self,third_from,cinema_index=1,num=1,seq_no=None,third_id=None,seat_index=1,mode=0):
        '''
        @description: 座位信息获取
        @notes: 
        @input: 
            third_from : 合作方
            cinema_index : 选择的满足条件的场次序号
            num ： 座位数
            seq_no : 场次号，仅在mode=1时有效；
            third_id : 第三方影院id，仅在mode=1时有效；
            seat_index : 座位序号，即返回第几个符合条件的座位，仅在mode=1时有效；
            mode: 0为检索模式，函数会搜索数据库并自动找出一个符合条件的场次；1为指定模式，需要用户指定seq_no、third_id和seat_index; 2为探测模式，仅对座位图获取请求成功与否做判断并返回结论
        @output：
            result : 座位信息，包括场次号、影院第三方id、座位号。
        '''
        result = {}
        result['seat_no'] = []
        #错误号。0：正常；1001：座位图获取失败；1002：场次已满
        result['error_no'] = 0
        if mode == 0:
            for i in range(10):
                schedule = self.getSchedule(third_from,cinema_index+i)
                if not schedule or not schedule['seq_no']:
                    logger.error('get schedule error for '+str(third_from))
                    continue

                result['seq_no'] = schedule['seq_no']
                result['third_id'] = schedule['third_id']
                if schedule.has_key('price'):
                    result['price'] = schedule['price']
                result['origin_price'] = schedule['origin_price']
                result['movie_id'] = schedule['movie_id']
                # fire老锁座接口需要hall_id,section_id,show_seq_no三个参数
                if schedule.has_key('hall_id'):
                    result['hall_id'] = schedule['hall_id']
                if schedule.has_key('section_id'):
                    result['section_id'] = schedule['section_id']
                if schedule.has_key('show_seq_no'):
                    result['show_seq_no'] = schedule['show_seq_no']
                #base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/' + 'seat/get'
                base_url = self.base_url + 'seat/get'
                params = {"third_from":schedule['third_from'],"seq_no":schedule['seq_no'],"third_id":schedule['third_id']}
                #logger.info('choose seq_no is http://' + ODP_PAL_SERVER['HOST'] + ':' + ODP_PAL_SERVER['PORT'] + '/detail?qt=movie&act=select&from=pc&seq_no='
                #    +schedule['seq_no']+ '&cinema_id='+ schedule['third_id'] +'&third_from='+schedule['third_from']+'&sfrom=map')
                while True:
                    seat_info = self.doRequest(base_url,params)
                    #logger.debug('seat_info is '+ str(seat_info));
                    if not seat_info.has_key('erroring'):
                        break


                # 取得没有预订的座位号
                if not 'data' in seat_info or not seat_info['data']:
                    logger.error('get seat info error for '+str(params));
                    continue
        else:
            if not seq_no or not third_id:
                return result
            result['seq_no'] = seq_no
            result['third_id'] = third_id
            #base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/' + 'seat/get'
            base_url = self.base_url + 'seat/get'
            params = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id}
            while True:
                #base_url='http://dianying.baidu.com/ticket/seat/get' # debug
                seat_info = self.doRequest(base_url,params)
                if not seat_info.has_key('erroring'):
                    break
            if not seat_info.has_key('data') or not seat_info['data']:
                logger.error('get seat info error for '+str(params));
                result['error_no'] = 1001
                return result
            if mode == 2:
                return result

        # 遍历场次座位信息，找到空余座位
        seq_full = 1
        for row in seat_info['data']:
            for col in row['col']:
                if col['sno'] and col['cid'] and col['st'] == 1:
                    seq_full = 0
                    seat_index -= 1
                    if seat_index <= 0:
                        result['seat_no'].append(col['sno'])
                        num -= 1
                        if num == 0:
                            break
            if num == 0:
                break
        if seq_full == 1:
            result['error_no'] = 1002
        return result
        
    def lockSeat(self,third_from,cinema_index=1,num=1,seq_no=None,third_id=None,seat_index=1,log_id=123456,phone_number='13892396551',mode=0):
        '''
        @description: 锁座
        @notes:
        @input: 
            third_from : 合作方
            cinema_index : 选择的满足条件的场次序号
            num : 座位数
            seq_no : 场次号，仅在mode=1时有效；
            third_id : 第三方影院id，仅在mode=1时有效；
            seat_index : 座位序号，仅在mode=1时有效；
            mode : 0是检索模式，会从数据库中自动选择一个合适的场次进行锁座；1是指定模式，会对指定场次和影院进行锁座
        @output：
            result : 座位信息，包括场次号、影院第三方id、座位号、第三方订单id。
        '''
        result = {}
        result['error_no'] = 0

        # 随机生成一个手机号
        phone_number = self.randomPhoneNum()
        result['phone_number'] = phone_number

        if mode == 0:
            for i in range(10):
                #获取座位
                seat_query = self.getSeat(third_from,cinema_index=1+i,num=num)
                if seat_query['error_no'] != 0:
                    continue
                seq_no = seat_query['seq_no']
                third_id = seat_query['third_id']
                seat_info = ''
                for seat_no in seat_query['seat_no']:
                    seat_info += '|' + seat_no
                seat_info = seat_info[1:]
                params = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id,"log_id":log_id,"phone_number":phone_number,"seat_info":seat_info}
                #base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/' + 'seat/lockseat'
                base_url = self.base_url + 'seat/lockseat'

                logger.info('lockseat seat info is '+ str(params) + ' , pc entry url is ' + \
                            'http://' + ODP_PAL_SERVER['HOST'] + ':' + ODP_PAL_SERVER['PORT'] + '/detail?qt=movie&act=select&from=pc&seq_no='\
                         +str(seq_no) + '&cinema_id='+ str(third_id) +'&third_from='+str(third_from)+'&sfrom=map');
                # 重试机制
                retry_max = 3
                retry = 0
                # 跳出重试的原因，0为锁座成功，1为超过重试次数
                break_reason = 0
                while True:
                    if retry == retry_max:
                        break_reason = 1
                        break
                    while True:
                        seat_lock = self.doRequest(base_url,params)                        
                        if not seat_lock.has_key('erroring'):
                            break
                    #print seat_lock
                    if seat_lock['third_order_id']:
                        break_reason = 0
                        break
                    retry += 1
                    time.sleep(1.5)

                if break_reason == 1:
                    logger.error('lockseat error')
                    continue

                third_order_id = seat_lock['third_order_id']
                result['seq_no'] = seq_no
                result['third_id'] = third_id
                result['seat_no'] = seat_info
                result['third_order_id'] = third_order_id
                return result
        elif mode == 1:
            seat_query = self.getSeat(third_from,seq_no=seq_no,third_id=third_id,seat_index=seat_index,mode=1)
            if seat_query['error_no'] != 0:
                result['error_no'] = seat_query['error_no']
                return result
            if seat_query['error_no'] == 0 and len(seat_query['seat_no']) == 0:
                result['error_no'] = 2001
                return result
            seq_no = seat_query['seq_no']
            third_id = seat_query['third_id']
            seat_info = ''
            for seat_no in seat_query['seat_no']:
                seat_info += '|' + seat_no
            seat_info = seat_info[1:]
            result['seq_no'] = seq_no
            result['third_id'] = third_id
            result['seat_no'] = seat_info
            params = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id,"log_id":log_id,"phone_number":phone_number,"seat_info":seat_info}
            #base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/' + 'seat/lockseat'
            base_url = self.base_url + 'seat/lockseat'
            # 重试机制
            retry_max = 5
            retry = 0
            while True:
                if retry == retry_max:
                    return result
                while True:
                    seat_lock = self.doRequest(base_url,params)
                    #print seat_lock
                    if not seat_lock.has_key('erroring'):
                        break
                if seat_lock.has_key('third_order_id') and seat_lock['third_order_id']:
                    break
                retry += 1
                time.sleep(1.5)
            third_order_id = seat_lock['third_order_id']
            #result['seq_no'] = seq_no
            #result['third_id'] = third_id
            #result['seat_no'] = seat_info
            result['third_order_id'] = third_order_id
            return result
        else:
            return result
            
    def getOrder(self,third_from):
        '''
        @description: 获取订单信息
        @notes: 
        @input: 
            third_from : 合作方
        @output：
            result : 订单信息，包括订票手机号。
        '''
        result = {}
        mysql = MySQLdb.connect(host=MYSQL['HOST'],port=MYSQL['PORT'],db=MYSQL['DB'],user=MYSQL['USER'],passwd=MYSQL['PASSWD'],charset='utf8')
        cursor = mysql.cursor()
        sql = "select * from t_movie_border where third_from='%s' order by border_id desc limit 0,1" % third_from
        #print sql
        cursor.execute(sql)
        for order in cursor.fetchall():
            result['phone_number'] = order[11]
            #print result['phone_number']
            if result['phone_number']:
                return result

    def getSeatStatus(self,third_from,seq_no,third_id,seat_no):
        '''
        @description: 座位锁定情况查询
        @notes: 目前仅支持单个座位查询
        @input: 
            third_from : 合作方
            seq_no : 场次号
            third_from ： 第三方影院id
            seat_no: 座位号
        @output：
            result : lock_status：座位锁定情况，0为走廊，1为可售，2为不可售，3为未找到座位
        '''
        result = {}
        result['error_no'] = 0
        if not seq_no or not third_id:
            return result
        #base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/' + 'seat/get'
        base_url = self.base_url + 'seat/get'
        params = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id}
        while True:
            seat_info = self.doRequest(base_url,params)
            if not seat_info.has_key('erroring'):
                break
        if not seat_info.has_key('data') or not seat_info['data']:
           logger.info(seat_info)
           result['error_no'] = 1001
           return result
        # 遍历场次座位信息，找到指定座位
        result['lock_status'] = 3
        for row in seat_info['data']:
            for col in row['col']:
                #if col['sno'] and col['cid'] and col['st'] == 1:
                if col['sno'] == seat_no:
                    result['lock_status'] = col['st']

        return result

    def randomPhoneNum(self):
        '''
        @description: 随机生成一个手机号
        @notes: 道高一尺，魔高一丈！
        @input:
        @output：
            phone_num:随机生成的手机号
        '''
        phone_num = '13'
        for i in range(9):
            digit = random.randint(0,9)
            phone_num += str(digit)
        return phone_num

 
    def getAllSchedules(self,third_from):
        '''
        @description: 获取某合作方的所有2小时以后的场次信息
        @notes: 
        @input: 
            third_from : 合作方
        @output：
            result : 场次信息，包括合作方名称、场次号、影院第三方id。
        '''
        result = []
        mysql = MySQLdb.connect(host=MYSQL["HOST"],port=MYSQL["PORT"],user=MYSQL["USER"],passwd=MYSQL["PASSWD"],db=MYSQL["DB"],charset="utf8")
        cursor = mysql.cursor()
        cmd = "select * from t_movie_cache_odp where third_from='%s' and data!='' order by id" % (third_from)
        cursor.execute(cmd)
        for item in cursor.fetchall():
            third_id = item[1]
            # debug for lanhai
            #if third_id != '32012101':
            #    continue
            try:
                time_table = json.loads(item[3])['time_table']
            except:
                continue
            refer_dict = {}
            if len(time_table) == 0 or type(time_table) == type(refer_dict):
                continue
            time_threshold = time.time()+2*60*60
            
            for day in range(len(time_table)):
                for seq in time_table[day]:
                    if not seq['time'] or not seq['date']:
                        continue
                    seq_datetime = seq['date'] + ' ' + seq['time']
                    try:
                        seq_outbuy_time = time.mktime(time.strptime(seq_datetime, '%Y-%m-%d %H:%M'))
                    except:
                        seq_outbuy_time = time.mktime(time.strptime(seq_datetime, '%Y-%m-%d %H:%M:%S'))
                    if seq_outbuy_time < time_threshold:
                        continue
                    if not seq['src_info'][0]['seq_no']:
                        continue 
                    
                    seq_info = {}
                    seq_info['seq_no'] = seq['src_info'][0]['seq_no']
                    seq_info['origin_price'] = seq['origin_price']
                    seq_info['third_from'] = third_from
                    seq_info['third_id'] = third_id
                    seq_info['movie_id'] = seq['src_info'][0]['movie_id']
                    seq_info['seq_outbuy_time'] = seq_outbuy_time
                    if seq['src_info'][0].has_key('price'):
                        seq_info['price'] = seq['src_info'][0]['price']
                    # fire锁座老接口需要的参数
                    if seq['src_info'][0].has_key('hall_id'):
                        seq_info['hall_id'] = seq['src_info'][0]['hall_id']
                    if seq['src_info'][0].has_key('section_id'):
                        seq_info['section_id'] = seq['src_info'][0]['section_id']
                    if seq['src_info'][0].has_key('show_seq_no'):
                        seq_info['show_seq_no'] = seq['src_info'][0]['show_seq_no']
                    result.append(seq_info)
                    #print seq
        return result

    def lockAllSeat(self,third_from,seq_no=None,third_id=None,mode=1):
        '''
        @description: 锁定某场次全部座位，并把结果
        @notes: 
        @input: 
            third_from : 合作方
            seq_no : 场次号，仅在mode=1时有效；
            third_id : 第三方影院id，仅在mode=1时有效；
            mode: 1为指定模式，需要用户指定seq_no、third_id
        @output：
            result : fail：失败次数； success：成功次数。
        '''
        result = {}
        result['seat_no'] = []
        #错误号。0：正常；1001：座位图获取失败；1002：场次已满
        result['error_no'] = 0
        result['fail'] = 0
        result['success'] = 0
        if mode == 1:
            if not seq_no or not third_id:
                return result
            result['seq_no'] = seq_no
            result['third_id'] = third_id
            #base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/' + 'seat/get'
            base_url = self.base_url + 'seat/get'
            params = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id}
            while True:
                #base_url='http://dianying.baidu.com/ticket/seat/get' # debug
                seat_info = self.doRequest(base_url,params)
                if not seat_info.has_key('erroring'):
                    break
            if not seat_info.has_key('data') or not seat_info['data']:
                logger.info(seat_info)
                result['error_no'] = 1001
                return result
        else:
            return result
        # 遍历场次座位信息，找到空余座位
        seq_full = 1
        for row in seat_info['data']:
            for col in row['col']:
                if col['sno'] and col['cid'] and col['st'] == 1:
                    seq_full = 0
					# 执行锁座
                    params = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id,"log_id":'123456',"phone_number":self.randomPhoneNum(),"seat_info":col['sno']}
                    base_url = self.base_url + 'seat/lockseat'
                    seat_lock = self.doRequest(base_url,params)
                    
                    if seat_lock.has_key('third_order_id') and seat_lock['third_order_id']:
                        result['success'] += 1
                        self.redis.incr(REDIS_CONF['SUC_NO']+'_lockseat')
                    elif seat_lock.has_key('erroring') and seat_lock['erroring'] == 2:
                        logger.error("::::time out!!!::::")
                        result['fail'] += 1
                        self.redis.incr(REDIS_CONF['FAIL_NO']+'_lockseat')
                    else:
                        logger.error("::::fail!!!::::")
                        result['fail'] += 1
                        self.redis.incr(REDIS_CONF['FAIL_NO']+'_lockseat')

        if seq_full == 1:
            result['error_no'] = 1002
        return result
		

    def setTimeout(self,time_out_seconds):
        socket.setdefaulttimeout(time_out_seconds)

 
if __name__ == '__main__':
    base = Ticket_Base()
    #print base.getSchedule('newvista')
    print base.getSeat('xingmei')
    #print base.getSeat(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3],seat_index=45,mode=1)
    #print base.getSeat('newvista',seq_no='0000000000005476',third_id='dadi0076',mode=2)
    #print base.lockSeat(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3],seat_index=int(sys.argv[4]),mode=1)
    #print base.lockSeat(sys.argv[1])
    #print base.lockSeat('lanhai',seq_no='151000693975',third_id='32012101',seat_index=1,mode=1)
    #print base.getSeatStatus('wangpiao',seq_no='16538746',third_id='1032',seat_no='11690721$11690721_1_14')
    #print base.signGenerate({"orderId":"txpcBDMO000023478","status":"PAY_SUCCESS","reduction":"0","requestId":"1234567","totalAmount":"1","paidAmount":"1"})
    #print base.lockSeat('shiguang')
    #print base.randomPhoneNum()
    #print base.lockAllSeat('newvista','0000000000004878','dadi0201')
    #print len(base.getAllSchedules('newvista'))
