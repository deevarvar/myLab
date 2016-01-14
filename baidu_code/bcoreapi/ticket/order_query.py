#-*- coding=utf-8 -*-
'''
@description: 核心购票新接口——订单查询接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
from base import Ticket_Base

class Ticket_Order_Query(Ticket_Base):
#@参数说明：
#@phone_number : 订座手机号
    def __init__(self,phone_number=None,third_from=None):
        super(Ticket_Order_Query,self).__init__()
        self.req_url = self.req_url + 'api/orderInfoForUser'
        if not phone_number:
            # 若没有输入phone_number,则需要查询order表获取手机号
            order = self.getOrder(third_from)
            phone_number = order['phone_number']
        else:
            pass
            
        self.req_dict = {"phone_number":phone_number}
        self.phone_number = phone_number
            

    def doAssert(self):
        #print self.page_dict
        assert int(self.page_dict['errorNo']) == 0
        assert self.page_dict['totalCount']
        assert self.page_dict['content']
        for content in self.page_dict['content']:
            assert content['orderId']
            assert content['orderStatus']
            assert content['totalPrice']
            assert content['thirdFrom']
            assert content['from']
            assert content['createTime']
            #assert content['cinemaName']
            assert content['seqNo']
            assert content['movieName']
            #assert content['theaterName']
            #assert content['showTime']
            assert content['smsNotifyTime']
            assert content['mobile']

if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Order_Query(phone_number=sys.argv[1])
        case.execute()
    else:
        #case = Ticket_Order_Query(phone_number='15800807450')
        is_success = 0
        for retry in range(3):
            case = Ticket_Order_Query(phone_number='15800807450')
            try:
                case.execute()
                is_success = 1
                break
            except:
                continue
        assert is_success == 1
