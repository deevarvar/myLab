#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——影院评论接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Info_Cinema_Comment(Info_Base):
    def __init__(self,cinema_id,pn,rn):
        super(Info_Cinema_Comment,self).__init__()
        self.req_url = self.req_url + 'cinemacomment'
        self.req_dict = {"cinema_id":cinema_id,"pn":pn,"rn":rn}
        self.cinema_id = cinema_id
        self.pn = pn
        self.rn = rn

    def doAssert(self):
        #print self.page_dict['errorMsg']
        assert self.page_dict['errorMsg'] == 'Success'
        assert self.page_dict.has_key('cinema_id') and self.page_dict['cinema_id'] == self.cinema_id
        assert self.page_dict.has_key('num')
        assert len(self.page_dict['data']) <= self.rn
        for data in self.page_dict['data']:
            assert data.has_key('id') and data['id']
            assert data.has_key('comment') and data['comment']
            assert data.has_key('comment_from') and data['comment_from']
            assert data.has_key('comment_from_name') and data['comment_from_name']
            assert data.has_key('comment_time')
            assert data.has_key('update_time')
            assert data.has_key('status') and (data['status'] == 0 or data['status'] == 1)

if __name__ == '__main__':
     
    case = Info_Cinema_Comment(7,1,10)
    case.execute()
