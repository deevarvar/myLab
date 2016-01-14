#-*- coding=utf-8 -*-
'''
@description: fire旧锁座接口测试用例。
@author: miliang<miliang@baidu.com>

'''

import sys
import time
import urllib
from settings import SERVER,ODP_PAL_SERVER,PAGE_SIGN_KEY,SIGN_KEY
from old_lock_seat import Ticket_Old_Lock_Seat

class Ticket_Old_Lock_Seat_Fire(Ticket_Old_Lock_Seat):
#@参数说明：
#@third_from : 合作方
#@seq_no : 场次号
#@third_id : 第三方影院id
#@log_id : 日志id
#@phone_number : 手机号
#@cinema_index ：若没有输入seq_no或third_id，该参数决定选择符合条件的第几个场次
#@num : 锁座数
    def __init__(self,third_from='fire',seq_no=None,third_id=None,phone_number='15800807450',cinema_index=1,num=1,device='pc'):
        self.req_url = 'http://' + ODP_PAL_SERVER['HOST'] + ':' + ODP_PAL_SERVER['PORT'] + '/movie/ticket/confirm/' + third_from +'/' + device
        self.base_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/ticket/'
        self.sign_key = SIGN_KEY
        if not seq_no or not third_id:
            seat_query = self.getSeat(third_from,cinema_index,num)
            seq_no = seat_query['seq_no']
            third_id = seat_query['third_id']
        else:
            pass
            #seat_query = self.getSeat(third_from,cinema_index,num,third_id,seq_no)
            
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
        self.req_dict['SeatNo'] = seat_info.split('$')[0]
        self.req_dict['SeatInfo'] = seat_info.split('$')[1]
        self.req_dict['TotalPrice'] = '%.2f' % float(seat_query['origin_price'])
        self.req_dict['Mobile'] = phone_number
        self.req_dict['time'] = int(time.time())
        self.req_dict['hallId'] = seat_query['hall_id']
        self.req_dict['sectionId'] = seat_query['section_id']
        if seat_query.has_key('show_seq_no'):
            self.req_dict['showSeqNo'] = seat_query['show_seq_no']
        #生成签名
        sign_dict = {'seq_no':seq_no,'movie_id':self.req_dict['MovieId'],'third_id':third_id,'ticket_price':int(seat_query['origin_price'])*100}
        self.req_dict['pagesign'] = self.GenPageSign(sign_dict)
        print self.req_dict
        
    
if __name__ == '__main__':
    if len(sys.argv) == 2: 
            case = Ticket_Old_Lock_Seat_Fire(sys.argv[1])
    elif len(sys.argv) == 3:
        case = Ticket_Old_Lock_Seat_Fire(sys.argv[1],num=int(sys.argv[2]))
    elif len(sys.argv) == 4:
        case = Ticket_Old_Lock_Seat_Fire(sys.argv[1],num=int(sys.argv[2]),cinema_index=(int(sys.argv[3])))
    elif len(sys.argv) == 5:
        case = Ticket_Old_Lock_Seat_Fire(sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3])
    else:
        case = Ticket_Old_Lock_Seat_Fire(third_from='fire')
    case.execute()
