#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rsphelper
from rsphelper import RspHelper
import sys
import time
import logging

class cmtsRsp(RspHelper):
    def __init__(self, third, configfile):
        RspHelper.__init__(self, third, configfile)
        self.orderno = 'soap_cmts' + str(int(time.time()*1000000))

    def seatinfo_rsp(self, rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp = '<?xml version=\"1.0\"?>\
                <GetPlanSiteStateResult>\
                    <ResultCode>0</ResultCode>\
                    <PlanSiteStates>\
                        <PlanSiteState>\
                            <SeatNo>05010526</SeatNo>\
                            <SeatState>1</SeatState>\
                            <SeatPieceNo>01</SeatPieceNo>\
                            <GraphRow>5</GraphRow>\
                            <GraphCol>26</GraphCol>\
                            <SeatRow>5</SeatRow>\
                            <SeatCol>9</SeatCol>\
                            <SeatPieceName>&#x5168;&gt;&#x533A;</SeatPieceName>\
                            <HallNo>05</HallNo>\
                        </PlanSiteState>\
                    </PlanSiteStates>\
                </GetPlanSiteStateResult>'
        else:
            #change ResultCode
            rsp = '<?xml version=\"1.0\"?>\
                <GetPlanSiteStateResult>\
                    <ResultCode>100500</ResultCode>\
                </GetPlanSiteStateResult>'
        return rsp

    def lockseat_rsp(self , rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp = '<?xml version=\"1.0\" encoding=\"utf-8\"?>\
                    <RealCheckSeatStateResult xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
                    <ResultCode>0</ResultCode>\
                    <OrderNo>'+ self.orderno +'</OrderNo>\
                    <SeatInfos>\
                        <SeatInfo>\
                            <SeatNo>04010117</SeatNo>\
                            <TicketPrice>30</TicketPrice>\
                            <SeatRow>1</SeatRow>\
                            <SeatCol>1</SeatCol>\
                            <SeatPieceNo>01</SeatPieceNo>\
                        </SeatInfo>\
                    </SeatInfos>\
                    </RealCheckSeatStateResult>'
        else:
            rsp = '<?xml version=\"1.0\" encoding=\"utf-8\"?>\
                    <RealCheckSeatStateResult xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
                    <ResultCode>101102</ResultCode>\
                    </RealCheckSeatStateResult>'
        return rsp

    def confirmorder_rsp(self, rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp = '<?xml version=\"1.0\"?>\
                <SellTicketResult xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
                  <ResultCode>0</ResultCode>\
                  <OrderNo>' + self.orderno +'</OrderNo>\
                  <ValidCode>104109</ValidCode>\
                </SellTicketResult>'
        else:
            rsp = '<?xml version=\"1.0\"?>\
                <SellTicketResult xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
                  <ResultCode>101257</ResultCode>\
                </SellTicketResult>'
        return rsp

    def queryorder_rsp(self, rsptype):
        rsp = ''
        if rsptype == self.CORRECT:
            rsp = '<?xml version=\"1.0\"?>\
                <GetOrderStatusResult xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
                  <ResultCode>0</ResultCode>\
                <OrderNo>'+ self.orderno +'</OrderNo>\
                <ValidCode>104109</ValidCode>\
                <OrderStatus>8</OrderStatus>\
                </GetOrderStatusResult>'
        elif rsptype == self.WRONG:
            rsp = '<?xml version=\"1.0\"?>\
                <GetOrderStatusResult xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
                  <ResultCode>0</ResultCode>\
                <OrderStatus>6</OrderStatus>\
                </GetOrderStatusResult>'
        else:
            rsp = '<?xml version=\"1.0\"?>\
                <GetOrderStatusResult xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
                  <ResultCode>0</ResultCode>\
                <OrderStatus>4</OrderStatus>\
                </GetOrderStatusResult>'
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
    cmts_rsp =  cmtsRsp('cmts', rsphelper.PROJECT_PATH + 'conf/cmts.conf')
    cmts_rsp.getdelaytime('lock_seat')
    rsp = cmts_rsp.genRsp('lock_seat')
    PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../")
    sys.path.append(PROJECT_PATH + 'lib')
    import settings
    logging.config.dictConfig(settings.LOGGING)
    logger = logging.getLogger('mockserver')
    logger.info(rsp)