#-*- coding=utf-8 -*-
'''
@description: 核心购票新接口——万达订单查询接口测试用例。
@note: 这个接口查的是order表。 
       自动查询订单号的功能还没有写好，目前仅支持手动输入订单号的方式
@author: miliang<miliang@baidu.com>

'''

import sys
from base import Ticket_Base

class Ticket_Order_Query(Ticket_Base):
    def __init__(self,third_order_id=None,order_index=1,log_id=123456):
        super(Ticket_Order_Query,self).__init__()
        self.req_url = self.req_url + 'order/wanda'
        # 若没有填写third_order_id，需要从数据库去查。
        if not third_order_id:
            #third_order_id = self.getOrder('wanda',order_index)
            third_order_id = self.getOrder('wanda')

        self.req_dict = {"third_order_id":third_order_id,"log_id":log_id}
        self.third_order_id = third_order_id
        self.log_id = log_id
            

    def doAssert(self):
        print self.page_dict
        assert self.page_dict['errorNo'] == 0


if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Order_Query(third_order_id=sys.argv[1])
    elif len(sys.argv) == 3:
        case = Ticket_Order_Query(third_order_id=sys.argv[1],order_index=int(sys.argv[2]))
    else:
        case = Ticket_Order_Query()
    case.execute()
