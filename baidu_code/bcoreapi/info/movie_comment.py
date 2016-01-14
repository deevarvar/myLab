#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——影片评论接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Info_Movie_Comment(Info_Base):
    def __init__(self,movie_id,pn,rn):
        super(Info_Movie_Comment,self).__init__()
        self.req_url = self.req_url + 'moviecomment'
        self.req_dict = {"movie_id":movie_id,"pn":pn,"rn":rn}
        self.movie_id = movie_id
        self.pn = pn
        self.rn = rn

    def doAssert(self):
        #print self.page_dict['errorMsg']
        assert self.page_dict['errorMsg'] == 'Success'
        assert self.page_dict.has_key('movie_id') and self.page_dict['movie_id'] == self.movie_id
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
     
    case = Info_Movie_Comment(3328,1,10)
    case.execute()
