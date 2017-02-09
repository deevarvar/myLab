#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
#record important event
#write once and pass, Orz~~

import re
import json
import os
import sys
import re

'''
    the report event structure is like
    [
        {
            ename: "s2b failed",
            enamecount: 1,
            errorlist: [
                {
                    "error": "ping error",
                    "errorcount": 1
                },
                {
                    "error": "dpd error",
                    "errorcount": 1
                },

            ]
        }
    ]
'''


#some utils functions used for event table
def name_in_list(tname, tkey,tlist):
    #etable is list
    if type(tlist) is list and len(tlist) > 0:
        for index, element in enumerate(tlist):
            if element[tkey] == tname:
                return True
    return False


def constructreportEvent(ename, errorstr):
    '''
    :param ename:
    :param errorstr:
    :return:
    '''

    newevent = dict()
    newevent['ename'] = ename
    newevent['enamecount'] = 1
    #errostr is a new list, may include different error str
    newevent['errorlist'] = list()
    if errorstr and len(errorstr):
        newerror = dict()
        newerror['error'] = errorstr
        newerror['errorcount'] = 1
        newevent['errorlist'].append(newerror)
    return newevent

def updatereportEvent(ename, errorstr, etable):
    '''
    1. update ename count
    2. update errorlist
    :param ename:
    :param errorstr:
    :param etable: all the event table
    :return:
    '''
    if type(etable) is list and len(etable) > 0:
        for index, element in enumerate(etable):
            if element['ename'] == ename:
                element['enamecount'] += 1
                #iterate the errorlist
                errorlist = element['errorlist']

                if type(errorlist) is list and len(errorlist) > 0:
                    for eindex, error in enumerate(errorlist):
                        if error['error'] == errorstr:
                            error['errorcount'] += 1
                            return
                    #if come here, so new error found
                    newerror = dict()
                    newerror['error'] = errorstr
                    newerror['errorcount'] = 1
                    errorlist.append(newerror)

    else:
        #no etable exist, so invoke new one.
        return constructreportEvent(ename, errorstr)