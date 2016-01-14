#-*- coding=utf-8 -*-
'''
@description: 核心购票新接口——座位图获取接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
import time
from base import Ticket_Base
from settings import NEW_PARTNER_SUPPORTED

class Ticket_Lock_Seat(Ticket_Base):
#@参数说明：
#@third_from : 合作方
#@seq_no : 场次号
#@third_id : 第三方影院id
#@log_id : 日志id
#@phone_number : 手机号
#@cinema_index ：若没有输入seq_no或third_id，该参数决定选择符合条件的第几个场次
#@num : 锁座数
    def __init__(self,third_from,seq_no=None,third_id=None,log_id=123456,phone_number='15800807450',cinema_index=1,num=1):
        super(Ticket_Lock_Seat,self).__init__()
        self.req_url = self.req_url + 'seat/lockseat'
        phone_number = self.randomPhoneNum()
        if not seq_no or not third_id:
            seat_query = self.getSeat(third_from,cinema_index,num)
            seq_no = seat_query['seq_no']
            third_id = seat_query['third_id']
        else:
            seat_query = self.getSeat(third_from,third_id=third_id,seq_no=seq_no,mode=1,num = num)
            
        seat_info = ''
        for seat_no in seat_query['seat_no']:
            seat_info += '|' + seat_no
        seat_info = seat_info[1:]
        print 'seat_info: ' + seat_info
        

        self.req_dict = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id,"log_id":log_id,"phone_number":phone_number,"seat_info":seat_info}
        self.third_from = third_from
        self.seq_no = seq_no
        self.third_id = third_id
        self.log_id = log_id
        self.phone_number = phone_number
        self.seat_info = seat_info
        print self.genUrl(self.req_url,self.req_dict)
            
    def execute(self):
        # 若接口返回的lock_status=3,引入重试机制查询出票最终状态
        retry_max = 1
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


    def doAssert(self):
        print self.page_dict
        assert int(self.page_dict['lock_status']) == 1 or int(self.page_dict['lock_status']) == 3
        # 若状态为3，则需再次请求同一个url确认锁座最终状态
        # TO DO...
        assert self.page_dict['third_order_id']


if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Lock_Seat(sys.argv[1])
        case.execute()
    elif len(sys.argv) == 3:
        case = Ticket_Lock_Seat(sys.argv[1],cinema_index=int(sys.argv[2]))
        case.execute()
    elif len(sys.argv) == 4:
        case = Ticket_Lock_Seat(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3])
        case.execute()
    elif len(sys.argv) == 5:
        case = Ticket_Lock_Seat(sys.argv[1],num=int(sys.argv[2]),cinema_index=(int(sys.argv[3])))
        case.execute()
    else:
        for partner in NEW_PARTNER_SUPPORTED:
            is_success = 0
            for retry in range(10):
                case = Ticket_Lock_Seat(third_from=partner,cinema_index=retry*10+1)
                try:
                    case.execute()
                    is_success = 1
                    break
                except:
                    continue
            assert is_success == 1
