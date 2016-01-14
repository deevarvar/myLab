#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——全部影院列表接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Info_Cinema_Index(Info_Base):
    def __init__(self,req_from):
        super(Info_Cinema_Index,self).__init__()
        self.req_url = self.req_url + 'allcinemas'
        self.req_dict = {"req_from":req_from}

    def doAssert(self):
        print self.page_dict
        assert self.page_dict['errorMsg'] == 'Success'
        #print self.page_dict['num']
        assert self.page_dict['num'] > 0
        assert len(self.page_dict['data']) == self.page_dict['num']
        #print self.page_dict['data'][0]
        for data in self.page_dict['data']:
            assert data.has_key('cinema_id') and data['cinema_id'] != 0
            assert data.has_key('name') and data['name'] != ''
            assert data.has_key('bid_encode') and data['bid_encode'] != ''
            assert data.has_key('bid') and data['bid'] != ''
            assert data.has_key('status') and (data['status']==0 or data['status']==1)

if __name__ == '__main__':
     
    case = Info_Cinema_Index('movie_c')
    case.execute()
