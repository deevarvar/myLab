#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——影讯详情接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Info_Movie_Detail(Info_Base):
    def __init__(self,movie_id):
        super(Info_Movie_Detail,self).__init__()
        self.req_url = self.req_url + 'moviedetail'
        self.req_dict = {"movie_id":movie_id}
        self.movie_id = movie_id

    def doAssert(self):
        print self.page_dict
        assert self.page_dict['errorMsg'] == 'Success'
        assert self.page_dict['data']
        assert self.page_dict['data'].has_key('movie_id') and self.page_dict['data']['movie_id'] == self.movie_id
        assert self.page_dict['data'].has_key('movie_name') and self.page_dict['data']['movie_name'] != ''
        assert self.page_dict['data'].has_key('works_id')
        assert self.page_dict['data'].has_key('movie_box_office')

if __name__ == '__main__':
     
    case = Info_Movie_Detail(3328)
    case.execute()
