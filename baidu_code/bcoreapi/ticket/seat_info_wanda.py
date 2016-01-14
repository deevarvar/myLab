#-*- coding=utf-8 -*-
'''
@description: 核心购票新接口——万达座位图获取接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
from base import Ticket_Base

class Ticket_Seat_Info_Wanda(Ticket_Base):
    def __init__(self,seq_no=None,third_id=None,cinema_index=1,phone_number='15800807450',callback='http://cp01-ocean-pool004.cp01.baidu.com:8888/detail?qt=movie',device='pc'):
        super(Ticket_Seat_Info_Wanda,self).__init__()
        self.req_url = self.req_url + 'seat/wanda'
        if not seq_no or not third_id:
            seq_info = self.getSchedule('wanda',cinema_index)
            seq_no = seq_info['seq_no']
            third_id = seq_info['third_id']

        self.req_dict = {"seq_no":seq_no,"third_id":third_id}
        if phone_number:
            self.req_dict['phone_number'] = phone_number
        if callback:
            self.req_dict['callback'] = callback
        if device:
            self.req_dict['device'] = device
            
        self.seq_no = seq_no
        self.third_id = third_id
        self.phone_number = phone_number
        self.callback = callback
            

    def doAssert(self):
        print self.page_dict
        assert self.page_dict['errorNo'] == 0
        assert self.page_dict['seat_url']


if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Seat_Info_Wanda(cinema_index=int(sys.argv[1]))
    elif len(sys.argv) == 3:
        case = Ticket_Seat_Info_Wanda(seq_no=sys.argv[1],third_id=sys.argv[2])
    elif len(sys.argv) == 4:
        case = Ticket_Seat_Info_Wanda(cinema_index=int(sys.argv[1]),phone_number=sys.argv[2],callback=sys.argv[3])
    else:
        #case = Ticket_Seat_Info('wangpiao','15199189','1133')
        #case = Ticket_Seat_Info('txpc','85709247','444')
        case = Ticket_Seat_Info_Wanda()
    case.execute()
