#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——影院详情接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Info_Cinema_Detail(Info_Base):
    def __init__(self,cinema_id):
        super(Info_Cinema_Detail,self).__init__()
        self.req_url = self.req_url + 'cinemadetail'
        self.req_dict = {"cinema_id":cinema_id}
        self.cinema_id = cinema_id

    def doAssert(self):
        #print self.page_dict
        assert self.page_dict['errorMsg'] == 'Success'
        assert self.page_dict['data']
        assert self.page_dict['data'].has_key('cinema_id') and self.page_dict['data']['cinema_id'] == self.cinema_id
        assert self.page_dict['data'].has_key('name') and self.page_dict['data']['name']
        assert self.page_dict['data'].has_key('bid') and self.page_dict['data']['bid']
        assert self.page_dict['data'].has_key('brand_id') and self.page_dict['data']['brand_id']
        assert self.page_dict['data'].has_key('brand_name') and self.page_dict['data']['brand_name']
        assert self.page_dict['data'].has_key('province') and self.page_dict['data']['province']
        assert self.page_dict['data'].has_key('province_id') and self.page_dict['data']['province_id']
        assert self.page_dict['data'].has_key('city_name') and self.page_dict['data']['city_name']
        assert self.page_dict['data'].has_key('city_id') and self.page_dict['data']['city_id']
        assert self.page_dict['data'].has_key('area') and self.page_dict['data']['area']
        assert self.page_dict['data'].has_key('area_id') and self.page_dict['data']['area_id']
        assert self.page_dict['data'].has_key('address') and self.page_dict['data']['address']
        assert self.page_dict['data'].has_key('alias')
        assert self.page_dict['data'].has_key('point_x') and self.page_dict['data']['point_x']
        assert self.page_dict['data'].has_key('point_y') and self.page_dict['data']['point_y']
        assert self.page_dict['data'].has_key('longitude') and self.page_dict['data']['longitude']
        assert self.page_dict['data'].has_key('latitude') and self.page_dict['data']['latitude']
        assert self.page_dict['data'].has_key('phone') and self.page_dict['data']['phone']
        assert self.page_dict['data'].has_key('shop_begin')
        assert self.page_dict['data'].has_key('shop_end')
        assert self.page_dict['data'].has_key('support_2D')
        assert self.page_dict['data'].has_key('support_3D')
        assert self.page_dict['data'].has_key('support_double3D')
        assert self.page_dict['data'].has_key('support_4D')
        assert self.page_dict['data'].has_key('support_4DX')
        assert self.page_dict['data'].has_key('support_reald')
        assert self.page_dict['data'].has_key('support_jumu')
        assert self.page_dict['data'].has_key('support_dolby')
        assert self.page_dict['data'].has_key('support_vip')
        assert self.page_dict['data'].has_key('support_pos')
        assert self.page_dict['data'].has_key('support_love_seat')
        assert self.page_dict['data'].has_key('support_wifi')
        assert self.page_dict['data'].has_key('is_book') and (self.page_dict['data']['is_book']==0 or self.page_dict['data']['is_book']==1)


if __name__ == '__main__':
     
    case = Info_Cinema_Detail(131)
    case.execute()
