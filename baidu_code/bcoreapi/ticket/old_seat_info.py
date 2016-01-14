#-*- coding=utf-8 -*-
'''
@description: 座位图获取老接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
from settings import ODP_PAL_SERVER,OLD_PARTNER_SUPPORTED
from base import Ticket_Base

class Ticket_Old_Seat_Info(Ticket_Base):
    def __init__(self,third_from,seq_no=None,third_id=None,cinema_index=1):
        super(Ticket_Old_Seat_Info,self).__init__()
        self.req_url = 'http://' + ODP_PAL_SERVER['HOST'] + ':' + ODP_PAL_SERVER['PORT'] + '/movie/ticket/seat/info'
        if not seq_no or not third_id:
            seq_info = self.getSchedule(third_from,cinema_index)
            seq_no = seq_info['seq_no']
            third_id = seq_info['third_id']

        self.req_dict = {"third_from":third_from,"seq_no":seq_no,"third_id":third_id}
        self.third_from = third_from
        self.seq_no = seq_no
        self.third_id = third_id
            

    def doAssert(self):
        print self.page_dict
        print self.third_from
        assert self.page_dict['errorNo'] == 0
        assert self.page_dict.has_key('seat_data')
        for data in self.page_dict['seat_data']:
            if data['row']:
                for col in data['col']:
                    assert col.has_key('st') and (col['st']==0 or col['st']==1 or col['st']==2)
                    assert col.has_key('sno')
                    if col['st']!=0:
                        assert col['sno']
                        assert col['cid']


if __name__ == '__main__':
    if len(sys.argv) == 2: 
        case = Ticket_Old_Seat_Info(sys.argv[1])
        case.execute()
    elif len(sys.argv) == 3:
        case = Ticket_Old_Seat_Info(sys.argv[1],cinema_index=int(sys.argv[2]))
        case.execute()
    elif len(sys.argv) == 4:
        print sys.argv[1]
        print sys.argv[2]
        print sys.argv[3]
        case = Ticket_Old_Seat_Info(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3])
        case.execute()
    else:
        for partner in OLD_PARTNER_SUPPORTED:
            is_success = 0
            for retry in range(5):
                case = Ticket_Old_Seat_Info(third_from=partner,cinema_index=retry*10+1)
                try:
                    case.execute()
                    is_success = 1
                    break
                except:
                    continue
            assert is_success == 1
