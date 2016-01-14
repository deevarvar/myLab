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
from fire_rsp import fireRsp
import settings

import logging

from wsgiref.simple_server import make_server

orderNo = ''

class fireService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode,Unicode, Unicode, Unicode, Unicode, Unicode, Unicode,_returns=Unicode)
    def qryTicket(ctx, userId, userPass,cinemaId, cinemaLinkId, hallId, sectionId, filmId, showSeqNo, showDate,showTime):
        rsp = fireRsp('fire', rsphelper.PROJECT_PATH + 'conf/fire.conf')
        seat = rsp.genRsp('seat_info')
        logger.info('fire seatinfo is ' + seat)
        return seat

    @rpc(Unicode, Unicode, Unicode, Unicode,Unicode, Unicode, Unicode, Unicode, Unicode, Unicode,Unicode, Unicode, Unicode, Unicode, Unicode,_returns=Unicode)
    def lockSeat( ctx, userId,  userPass,  orderNo,  ticketCount,  checkValue,  cinemaId,  cinemaLinkId,  hallId,  sectionId,  filmId,  showSeqNo,  showDate,  showTime,  seatId,  randKey):
        rsp = fireRsp('fire', rsphelper.PROJECT_PATH + 'conf/fire.conf')
        lockseat = rsp.genRsp('lock_seat')
        logger.info('fire lockseat is ' + lockseat)
        return lockseat

    @rpc(Unicode, Unicode, Unicode, Unicode,Unicode, Unicode, Unicode, Unicode, Unicode, Unicode,Unicode, Unicode, Unicode, Unicode, Unicode,Unicode, Unicode,_returns=Unicode)
    def fixOrder( ctx, userId,  userPass,  orderNo,  ticketCount,  checkValue,  cinemaId,  cinemaLinkId,  hallId,  filmId,  showSeqNo,  showDate,  showTime,  priceList,  feeList,  randKey,  payment,  paymentNo):
        rsp = fireRsp('fire', rsphelper.PROJECT_PATH + 'conf/fire.conf')
        sell = rsp.genRsp('confirm_order')
        logger.info('fire conformorder is ' + sell)
        return sell

    @rpc(Unicode, Unicode,Unicode, Unicode, Unicode, Unicode, Unicode, Unicode,_returns=Unicode)
    def qryOrder( ctx, userId,  userPass,  orderNo,  ticketCount,  checkValue,  cinemaId,  cinemaLinkId,  randKey):
        rsp = fireRsp('fire', rsphelper.PROJECT_PATH + 'conf/fire.conf')
        order = rsp.genRsp('query_order')
        logger.info('fire query_order is ' + order)
        return order


application = Application([fireService], 'http://interface.ykse.com/v4/',
                          in_protocol=Soap11(),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    
    #fixme, donot know why: change server method, need to change port and restart...
    port = 8006
    #logging.basicConfig(level=logging.DEBUG)
    #logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    logging.config.dictConfig(settings.LOGGING)
    global logger
    logger = logging.getLogger('mockserver')
    logger.info('start to listent to ' + str(port))

    server = make_server('', port, wsgi_application)

    server.serve_forever()
