#-*- coding=utf-8 -*-
'''
@description: 影讯新接口测试用例基类。
@author: miliang<miliang@baidu.com>

'''
import sys
import copy
import urllib
import urllib2
import json
import hashlib
import time
from base import Info_Base
from settings import SERVER,SIGN_KEY

class Online_Info_Util(Info_Base):
    def __init__(self):
        super(Online_Info_Util,self).__init__()
        self.req_url = 'http://dianying.baidu.com/info/api/'

if __name__ == '__main__':
    util = Online_Info_Util()
    params = {"cinema_id":1}
    print util.signGenerate(params)
    
