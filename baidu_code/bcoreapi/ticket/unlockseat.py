#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @description api to unlock seat
# @author yezhihua@baidu.com

import sys
import time
from base import Ticket_Base
from lock_seat import Ticket_Lock_Seat
from settings import NEW_PARTNER_SUPPORTED

import random
import ticketlog
import logging.config

from settings import ODP_PAL_SERVER

logging.config.dictConfig(ticketlog.LOGGING)
logger = logging.getLogger('ticket')

class TicketUnlockSeat(Ticket_Base):
    def __init__(self, third_from, seq_no = None, third_id = None,num=1):
        Ticket_Base.__init__(self)
        num = random.randint(1,4)
        self.third_from = third_from
        if not seq_no or not third_id:
            seat_lock = self.lockSeat(third_from = third_from, num=num)
        else:
            seat_lock = self.lockSeat(third_from,seq_no=seq_no,third_id=third_id,log_id=123456,mode=1,num= num)
        third_order_id = seat_lock['third_order_id']
        assert third_order_id != None
        self.req_url = self.req_url + 'seat/unlockseat'
        phone_number = self.randomPhoneNum()
        self.req_dict = {
            "third_from": third_from,
            "third_order_id": third_order_id,
            "log_id" : 123456
        }


    def execute(self):
        sleeptime = 3
        logger.info('sleep '+ str(sleeptime) +'s to see the result')
        time.sleep(sleeptime)
        self.page_dict = self.doRequest(self.req_url,self.req_dict)
        logger.info('lockseat rsp is' + str(self.page_dict))
        #{u'errorNo': 0, u'errorMsg': u'\u6210\u529f', u'unlock_status': 4}
        assert self.page_dict['errorNo'] == 0 and self.page_dict['unlock_status'] == 4
        logger.info(self.third_from + ' unlockseat successfully.')

        #try to unlock second time
        #{"errorNo":200013,"errorMsg":"\u5ea7\u4f4d\u89e3\u9501\u5931\u8d25","unlock_status":5}
        negative = self.doRequest(self.req_url,self.req_dict)
        logger.info('try to unlockseat unlocked seat rsp is' + str(negative))
        assert negative['errorNo'] == 200013 and negative['unlock_status'] == 5
        logger.info(self.third_from + 'unlockseat negative case passes')

if __name__ == '__main__':
    print 'argv len is ' + str(len(sys.argv))
    if len(sys.argv) == 1:
        logger.info('iterate all the third_from.')
        all_third = ['spider','shiguang','jinyi',
                     'fire','lanhai','cmts','maizuo', 'dingxin','xingmei','wangpiao','vista','chenxing','cfc',
                     'meijia','flamingo','lumiai','cgv','dadi', 'txpc']
        problem_third = ['1905']
        not_supported = ['wanda','cful', 'shidai']
        for third in all_third:
            logger.info('start to test '+ third)
            unlockseat = TicketUnlockSeat(third_from=third)
            unlockseat.execute();
    elif len(sys.argv) == 2:
        logger.info('choose avaiable cinema from db. ')
        unlockseat = TicketUnlockSeat(third_from=sys.argv[1])
        unlockseat.execute();
    elif len(sys.argv) == 4:
        #PC: http://cp01-ocean-pool001.cp01.baidu.com:8888/detail?qt=movie&act=select&from=pc&seq_no=600360214785458176&cinema_id=0001&third_from=dadi&sfrom=map
        #webapp: http://cp01-ocean-pool001.cp01.baidu.com:8204/ticket/select/dadi/webapp?qt=movie&act=select&seq_no=600360214856761344&cinema_id=0001&discountid=&third_from=dadi&istpl=1&sfrom=map&from=webapp
        logger.info('choose seq_no is http://' + ODP_PAL_SERVER['HOST'] + ':' + ODP_PAL_SERVER['PORT'] + '/detail?qt=movie&act=select&from=pc&seq_no='
                    +sys.argv[2]+ '&cinema_id='+ sys.argv[3]+'&third_from='+sys.argv[1]+'&sfrom=map')
        unlockseat = TicketUnlockSeat(third_from=sys.argv[1],seq_no=sys.argv[2],third_id=sys.argv[3])
        unlockseat.execute();
