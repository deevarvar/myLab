#-*- coding=utf-8 -*-
'''
@description: 旧支付渲染接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
import os
import time
import urllib
import urllib2
import json
import MySQLdb
from settings import SERVER,MYSQL,ODP_MOVIE_PATH
from base import Ticket_Base
from old_pay_notice import Ticket_Old_Pay_Notice

class Ticket_Old_Pay_Back(Ticket_Old_Pay_Notice):
    
    def __init__(self,third_from,third_order_id=None,cinema_index=1,num=1,seq_no=None,third_id=None,mode=0,device='pc'):
        Ticket_Old_Pay_Notice.__init__(self,third_from,third_order_id,cinema_index,num,seq_no,third_id,mode,device)
        self.req_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/payback/' + third_from + '/' + device

    def doAssert(self):
        assert self.page_dict['user_mobile']
        assert self.page_dict['detail']['movie_name']
        assert self.page_dict['detail']['phone']
        assert self.page_dict['detail']['seat_info']
        assert self.page_dict['detail']['total_price']
        assert self.page_dict['detail']['status']
        assert self.page_dict['detail']['seq_no']
        assert self.page_dict['detail']['order_id'] == self.third_order_id
        assert self.page_dict['detail']['payurl']


if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Old_Pay_Back(sys.argv[1])
    elif len(sys.argv) == 3:
        case = Ticket_Old_Pay_Back(sys.argv[1],third_order_id=sys.argv[2])
    elif len(sys.argv) == 4:
        #case = Ticket_Old_Pay_Back(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3],mode=1)
        case = Ticket_Old_Pay_Back(sys.argv[1],num=int(sys.argv[2]),cinema_index=int(sys.argv[3]))
    else:
        case = Ticket_Old_Pay_Back('maizuo')

    case.execute()
