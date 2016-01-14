#-*- coding=utf-8 -*-
'''
@description: 核心购票新接口——重发短信接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
from base import Ticket_Base

class Ticket_Resend_Message(Ticket_Base):
#@参数说明：
#@third_order_id : 第三方订单号
    def __init__(self,third_from=None,third_order_id=None):
        super(Ticket_Resend_Message,self).__init__()
        self.req_url = self.req_url + 'api/resendMessageForUser'
        if not third_order_id:
            # 若没有输入third_order_id,则需要查询order表获取订单信息
            #order = self.getOrder(third_from)
            #phone_number = order['phone_number']
            pass
            
        self.req_dict = {"third_from":third_from,"third_order_id":third_order_id}
        print self.page_dict
        self.third_from = third_from
        self.third_order_id = third_order_id
            

    def doAssert(self):
        print self.page_dict
        assert int(self.page_dict['errorNo']) == 0

if __name__ == '__main__':
    if len(sys.argv) == 3: 
        case = Ticket_Resend_Message(third_from=sys.argv[1],third_order_id=sys.argv[2])
    else: 
        case = Ticket_Resend_Message()
    case.execute()
