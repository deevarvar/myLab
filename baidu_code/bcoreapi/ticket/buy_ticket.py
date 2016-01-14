#-*- coding=utf-8 -*-
'''
@description: 核心购票新接口——出票接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
import time
from base import Ticket_Base

class Ticket_Buy_Ticket(Ticket_Base):
    def __init__(self,third_from,third_order_id=None,log_id=123456,cinema_index=1,num=1,seq_no=None,third_id=None,mode=0,is_mem_pay=0):
        super(Ticket_Buy_Ticket,self).__init__()
        self.req_url = self.req_url + 'trade/buy'
        # 若没有指定third_order_id，需要自行执行锁座并获取third_order_id
        if not third_order_id:
            if mode == 0:
                seat_lock = self.lockSeat(third_from,cinema_index,num,log_id)
                third_order_id = seat_lock['third_order_id']
            else:
                seat_lock = self.lockSeat(third_from,seq_no=seq_no,third_id=third_id,log_id=log_id,mode=1)
                third_order_id = seat_lock['third_order_id']

        self.req_dict = {"third_from":third_from,"third_order_id":third_order_id,"log_id":log_id,"is_mem_pay":is_mem_pay}
        self.third_from = third_from
        self.third_order_id = third_order_id
        self.log_id = log_id
        self.is_mem_pay = is_mem_pay
        
            


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

    def doAssert(self):
        print self.page_dict
        assert int(self.page_dict['errorNo']) == 0
        assert int(self.page_dict['buy_status']) == 1
        if int(self.page_dict['buy_status']) == 1:
            assert self.page_dict['sms_ticket_code']
           # assert self.page_dict['msg_content']


if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Buy_Ticket(sys.argv[1])
    elif len(sys.argv) == 3:
        case = Ticket_Buy_Ticket(sys.argv[1],third_order_id=sys.argv[2])
    elif len(sys.argv) == 4:
        case = Ticket_Buy_Ticket(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3],mode=1)
    elif len(sys.argv) == 5:
        case = Ticket_Buy_Ticket(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3],is_mem_pay=sys.argv[4],mode=1)
    else:
        case = Ticket_Buy_Ticket('maizuo')

    case.execute()
