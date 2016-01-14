#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rsphelper
from rsphelper import RspHelper
import sys
import time
import logging

class fireRsp(RspHelper):
    def __init__(self, third, configfile):
        RspHelper.__init__(self, third, configfile)
        self.orderno = 'soap_fire' +  str(int(time.time()*1000000))

    def seatinfo_rsp(self, rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
                           <showSeats cinemaId=\"00000003\" hallId=\"3\" version=\"1.0\"> \
                           <section id=\"01\" ><seat rowId=\"A\" columnId=\"17\" /><seat rowId=\"A\" columnId=\"18\" /> \
                           </section>\
                           </showSeats>'
        else:

            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
                           <showSeats></showSeats>'
        return rsp

    def lockseat_rsp(self , rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
                  <seatLock version=\"1.0\" > \
                  <result>0</result> \
                  <messages><message>Success</message></messages> \
                  <seats><seat rowId=\"A\" columnId=\"16\" statusInd=\"\" /> \
                  </seats></seatLock>'
        else:
            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
                  <seatLock version=\"1.0\" > \
                  <result>1</result> \
                  </seatLock>'
        return rsp

    def confirmorder_rsp(self, rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp ='<?xml version=\"1.0\" encoding=\"GBK\"?> \
                  <bookingConfirm version=\"1.0\"> \
                  <result>0</result> \
                  <bookingId>'+ self.orderno + '</bookingId> \
                  <messages><message>\u8ba2\u5355\u5904\u7406\u6210\u529f(OPS:Order Processed Successfully)</message></messages> \
                  <confirmationId>02360769</confirmationId> \
                  <seats><seat ticketNo=\"88881505000868\" rowId=\"A\" columnId=\"14\" sectionId=\"\" statusInd=\"\" printedFlg=\"\" lastModifyTime=\"\"/></seats> \
                  </bookingConfirm>'
        else:
            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
                  <bookingConfirm version=\"1.0\"> \
                  <result>6</result> \
                  </bookingConfirm>'
        return rsp

    def queryorder_rsp(self, rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
              <orderDetail version=\"1.0\"> \
              <cinemaId>00000003</cinemaId><hallId>3</hallId><filmId>00120551201301</filmId> \
              <show seqNo=\"\" date=\"2015-05-30\" time=\"1620\" /> \
              <seats><seat ticketNO=\"88881505000864\" sectionId=\"01\" rowId=\"A\" columnId=\"16\" statusInd=\"B\" printedFlg=\"N\" lastModifyTime=\"\"  infoCode=\"\"/></seats> \
              <result>0</result> \
              <messages><message>\u4ea4\u6613\u6210\u529f\uff0c\u8ba2\u5355\u5df2\u7ecf\u786e\u8ba4</message></messages> \
              <statusInd>1</statusInd><bookingId>' + self.orderno + '</bookingId> \
              <confirmationId>09160392</confirmationId></orderDetail>'
        elif rsptype == self.WRONG:
            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
              <orderDetail version=\"1.0\"> \
              <result>6</result> \
              </orderDetail>'
        else:
            rsp = '<?xml version=\"1.0\" encoding=\"GBK\"?> \
              <orderDetail version=\"1.0\"> \
              <result>-1</result> \
              </orderDetail>'
        return rsp

    def genRsp(self, api):
        #1.delay
        delaytime = self.getdelaytime(api)
        time.sleep(int(delaytime))
        #2. get rsp type
        rsptype = self.getrsptype(api)
        api_interface = {
            'seat_info' : self.seatinfo_rsp,
            'lock_seat' : self.lockseat_rsp,
            'confirm_order' : self.confirmorder_rsp,
            'query_order' : self.queryorder_rsp
        }
        rsp = api_interface[api](rsptype)
        return rsp

if __name__  == '__main__':
    fire_rsp =  fireRsp('rsp', rsphelper.PROJECT_PATH + 'conf/fire.conf')
    fire_rsp.getdelaytime('lock_seat')
    rsp = fire_rsp.genRsp('lock_seat')
    PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../")
    sys.path.append(PROJECT_PATH + 'lib')
    import settings
    logging.config.dictConfig(settings.LOGGING)
    logger = logging.getLogger('mockserver')
    logger.info(rsp)