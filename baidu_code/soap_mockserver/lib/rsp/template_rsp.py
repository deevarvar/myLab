#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rsphelper
from rsphelper import RspHelper
import sys
import time


class cmtsRsp(RspHelper):
    def __init__(self, third, configfile):
        RspHelper.__init__(self, third, configfile)
        self.orderno = 'a' + str(int(time.time()*1000000))
    def seatinfo_rsp(self, rsptype):
        rsp = dict()
        if rsptype == self.CORRECT:
            pass
        else:
            pass
        return rsp

    def lockseat_rsp(self,rsptype):
        rsp = dict()
        if rsptype == self.CORRECT:
            pass
        else:
            pass
        return rsp

    def confirmorder_rsp(self,rsptype):
        rsp = dict()
        if rsptype == self.CORRECT:
            pass
        else:
            pass
        return rsp

    def queryorder_rsp(self, rsptype):
        rsp = dict()
        if rsptype == self.CORRECT:
            pass
        elif rsptype == self.WRONG:
            pass
        else:
            pass
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
    #xingmei_rsp.getrsptype('lock_seat')