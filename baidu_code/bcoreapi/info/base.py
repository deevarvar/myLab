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
import MySQLdb
from settings import SERVER,MYSQL,SIGN_KEY

class Info_Base(object):
    def __init__(self):
        self.req_url = 'http://' + SERVER['HOST'] + ':' + SERVER['PORT'] + '/info/api/'
        self.req_dict = {}
        self.page_dict = {}

    def doAssert(self):
        pass

    def execute(self):
        self.page_dict = self.doRequest(self.req_url,self.req_dict)
        self.doAssert()
    
    def doRequest(self,base_url,params):
        sign = self.signGenerate(params)
        params['sign'] = sign
        query_string = urllib.urlencode(params)
        url = base_url + '?' + query_string
        print '::::Request url:::: ' + url
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        values = {'name' : 'Escaton','location' : 'China', 'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        data = urllib.urlencode(values)
        req = urllib2.Request(url,'',headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        try:
            return json.loads(the_page)
        except:
            assert 0>1
            return

    def signGenerate(self,params_origin):
        params = copy.deepcopy(params_origin)
        if params.has_key('log_id'):
            del params['log_id']
        if params.has_key('sign'):
            del params['sign']
        params = sorted(params.iteritems(), key=lambda d:d[0])
        sign = hashlib.new("md5", SIGN_KEY + urllib.urlencode(params)).hexdigest()
        sign = hashlib.new("md5", sign + SIGN_KEY).hexdigest()
        return sign

    def getAllCinemasBid(self):
        '''
        @description: 查询全部影院bid
        @notes:
        @input:
        @output：
            result : 所有影院bid值的数组
        '''
        mysql = MySQLdb.connect(host=MYSQL["HOST"],port=MYSQL["PORT"],user=MYSQL["USER"],passwd=MYSQL["PASSWD"],db=MYSQL["DB"],charset="utf8")
        cursor = mysql.cursor()
        cmd = "select bid from t_movie_cinemas"
        cursor.execute(cmd)

        result = []

        for item in cursor.fetchall():
            bid = item[0]
            result.append(bid)

        return result

if __name__ == '__main__':
    base = Info_Base()
    params = {"cinema_id":1}
    print base.getAllCinemasBid()
    #print base.signGenerate(params)
    
