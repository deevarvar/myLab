#!/usr/bin/env python
# encoding: utf8


"""
This is a simple HelloWorld example to show the basics of writing
a webservice using spyne, starting a server, and creating a service
client.

Here's how to call it using suds:

#>>> from suds.client import Client
#>>> c = Client('http://localhost:8000/?wsdl')
#>>> c.service.say_hello('punk', 5)
(stringArray){
   string[] =
      "Hello, punk",
      "Hello, punk",
      "Hello, punk",
      "Hello, punk",
      "Hello, punk",
 }
#>>>
"""
import os
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
import sys
sys.path.append(CURRENT_PATH)
import time
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJECT_PATH + '/lib')
sys.path.append(PROJECT_PATH + '/lib/rsp')
import rsphelper
from cmts_rsp import cmtsRsp
import settings

import logging

from wsgiref.simple_server import make_server

orderNo = ''

class CmtsService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def GetToken(ctx, pAppCode, pVerifyInfo):
        token = '<TokenResult><ResultCode>0</ResultCode><TokenID>1829</TokenID><Token>cmts_token</Token><TimeOut>300</TimeOut></TokenResult>'
        logger.info('enter getoken')
        return token

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def GetPlanCannotSellSeat(ctx, pAppCode, pFeatureAppNo, pSerial,pVerifyInfo):
        rsp = cmtsRsp('cmts', rsphelper.PROJECT_PATH + 'conf/cmts.conf')
        seat = rsp.genRsp('seat_info')
        logger.info('cmts seatinfo is ' + seat)
        return seat

    @rpc(Unicode, _returns=Unicode)
    def LiveRealCheckSeatState(ctx, pXmlString):
        rsp = cmtsRsp('cmts', rsphelper.PROJECT_PATH + 'conf/cmts.conf')
        lockseat = rsp.genRsp('lock_seat')
        logger.info('cmts lockseat is ' + lockseat)
        return lockseat

    @rpc(Unicode, _returns=Unicode)
    def SellTicket(ctx, pXmlString):
        rsp = cmtsRsp('cmts', rsphelper.PROJECT_PATH + 'conf/cmts.conf')
        sell = rsp.genRsp('confirm_order')
        logger.info('cmts conformorder is ' + sell)
        return sell

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def GetOrderStatus(ctx, pAppCode,pSerialNum, pTokenID, pVerifyInfo):
        rsp = cmtsRsp('cmts', rsphelper.PROJECT_PATH + 'conf/cmts.conf')
        order = rsp.genRsp('query_order')
        logger.info('cmts query_order is ' + order)
        return order

application = Application([CmtsService], 'http://webservice.main.cmts.cn',
                          in_protocol=Soap11(),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    
    #fixme, donot know why: change server method, need to change port and restart...
    port = 8005
    #logging.basicConfig(level=logging.DEBUG)
    #logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    logging.config.dictConfig(settings.LOGGING)
    global logger
    logger = logging.getLogger('mockserver')
    logger.info('start to listent to ' + str(port))

    server = make_server('', port, wsgi_application)

    server.serve_forever()
