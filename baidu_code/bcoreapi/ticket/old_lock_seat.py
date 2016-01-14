#-*- coding=utf-8 -*-
'''
@description: 旧锁座接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
import copy
import time
import hashlib
import urllib
from settings import OLD_PARTNER_SUPPORTED,ODP_PAL_SERVER,PAGE_SIGN_KEY
from base import Ticket_Base

class Ticket_Old_Lock_Seat(Ticket_Base):
#@参数说明：
#@third_from : 合作方
#@seq_no : 场次号
#@third_id : 第三方影院id
#@log_id : 日志id
#@phone_number : 手机号
#@cinema_index ：若没有输入seq_no或third_id，该参数决定选择符合条件的第几个场次
#@num : 锁座数
    def __init__(self,third_from=None,seq_no=None,third_id=None,phone_number='15800807450',cinema_index=1,num=1,device='pc'):
        super(Ticket_Old_Lock_Seat,self).__init__()
        self.req_url = 'http://' + ODP_PAL_SERVER['HOST'] + ':' + ODP_PAL_SERVER['PORT'] + '/movie/ticket/confirm/' + third_from +'/' + device
        if not seq_no or not third_id:
            seat_query = self.getSeat(third_from,cinema_index,num)
            seq_no = seat_query['seq_no']
            third_id = seat_query['third_id']
        else:
            seat_query = self.getSeat(third_from,seq_no=seq_no,third_id=third_id,mode=1)
            
        seat_info = ''
        for seat_no in seat_query['seat_no']:
            seat_info += '|' + seat_no
        seat_info = seat_info[1:]
        #print 'seat_info: ' + seat_info


        self.req_dict = {}
        self.req_dict['lock_ajax'] = 1
        self.req_dict['CinemaId'] = third_id
        self.req_dict['MovieId'] = seat_query['movie_id']
        self.req_dict['SeqNo'] = seq_no
        print seat_info
        self.req_dict['SeatNo'] = seat_info.split('$')[0]
        self.req_dict['SeatInfo'] = seat_info.split('$')[1]
        # 这里不能乱写，要写真实价格……
        if seat_query.has_key('price'):
            self.req_dict['TotalPrice'] = '%.2f' % float(seat_query['price'])
        else:
            self.req_dict['TotalPrice'] = '%.2f' % float(seat_query['origin_price'])
        self.req_dict['Mobile'] = phone_number
        self.req_dict['time'] = int(time.time())
        #生成签名
        #sign_dict = {'seq_no':seq_no,'movie_id':self.req_dict['MovieId'],'third_id':third_id,'ticket_price':int(float(seat_query['origin_price'])*100)}
        sign_dict = {'seq_no':seq_no,'movie_id':self.req_dict['MovieId'],'third_id':third_id,'ticket_price':int(float(self.req_dict['TotalPrice'])*100)}
        self.req_dict['pagesign'] = self.GenPageSign(sign_dict)
        print self.req_dict
        
    
    '''
    def execute(self):
        # 若接口返回的lock_status=3,引入重试机制查询出票最终状态
        retry_max = 5
        retry = 0
        while True:
            if retry == retry_max:
                break
            try:
                self.page_dict = self.doRequest(self.req_url,self.req_dict)
            except:
                retry += 1
                time.sleep(1.5)
                continue
            if not self.page_dict or not self.page_dict.has_key('lock_status'):
                retry += 1
                time.sleep(1.5)
                continue
            if int(self.page_dict['lock_status']) != 3:
                break
            retry += 1
            time.sleep(1.5)

        self.doAssert()
    '''

    def doAssert(self):
        print self.page_dict
        assert self.page_dict['page_data']['order_id']
        self.third_order_id = self.page_dict['page_data']['order_id']
        

    def GenPageSign(self,params_origin):
        params = copy.deepcopy(params_origin)
        params = sorted(params.iteritems(), key=lambda d:d[0])
        print "Sign string: " + urllib.urlencode(params) + PAGE_SIGN_KEY
        sign = hashlib.new("md5", urllib.urlencode(params) + PAGE_SIGN_KEY).hexdigest()
        return sign

if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Old_Lock_Seat(sys.argv[1])
        case.execute()
    elif len(sys.argv) == 3:
        case = Ticket_Old_Lock_Seat(sys.argv[1],num=int(sys.argv[2]))
    elif len(sys.argv) == 4:
        case = Ticket_Old_Lock_Seat(sys.argv[1],num=int(sys.argv[2]),cinema_index=(int(sys.argv[3])))
        case.execute()
    elif len(sys.argv) == 5:
        case = Ticket_Old_Lock_Seat(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3])
        case.execute()
    else:
        for partner in OLD_PARTNER_SUPPORTED:
            is_success = 0
            for retry in range(5):
                case = Ticket_Old_Lock_Seat(third_from=partner,cinema_index=retry*10+1)
                try:
                    case.execute()
                    is_success = 1
                    break
                except:
                    continue
            assert is_success == 1
