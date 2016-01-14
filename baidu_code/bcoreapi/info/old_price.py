#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——排期接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Old_Info_Price(Info_Base):
    def __init__(self,uid=None,device='webview',sfrom='map'):
        super(Old_Info_Price,self).__init__()
        self.req_url = self.req_url + 'price'
        self.req_dict = {}
        self.req_dict['uid'] = uid
        self.req_dict['from'] = device
        self.req_dict['sfrom'] = sfrom
        self.uid = uid
        self.device = device
        self.sfrom = sfrom

    def doAssert(self):
        #print self.page_dict
        assert self.page_dict['errorMsg'] == 'Success'
        #assert self.page_dict['base']
        #assert self.page_dict['time_table']
        if not self.page_dict['time_table']:
            return
        partner = ''
        for date in range(len(self.page_dict['time_table'])):
            for schedule in self.page_dict['time_table'][date]:
                assert schedule['time']
                assert schedule['date']
                assert schedule['movie_id']
                assert schedule['lower_price']
                assert schedule.has_key('src_info')
                for i in range(len(schedule['src_info'])):
                    assert schedule['src_info'][i]['src']
                    # 5.11:同一家影院只会提供一个合作方的影讯
                    if partner == '':
                        partner = schedule['src_info'][i]['src']
                    else:
                        assert schedule['src_info'][i]['src'] == partner

                    assert schedule['src_info'][i].has_key('lan') # 这个暂时可能为空
                    assert schedule['src_info'][i].has_key('type') # 这个暂时可能为空
                    #assert schedule['src_info'][i]['origin_price']
                    assert schedule['src_info'][i]['price']
                    assert schedule['src_info'][i].has_key('seq_no') # 这个暂时可能为空
                    assert schedule['src_info'][i]['cinema_id']
                    assert schedule['src_info'][i]['movie_id']
                    assert schedule['src_info'][i]['theater']
                    assert schedule['src_info'][i]['src_name']
                    assert schedule['src_info'][i]['out_buy_time'] 
                    assert schedule['src_info'][i].has_key('hall_id')    # 这个暂时可能为空



if __name__ == '__main__':
     
    case = Old_Info_Price(uid='6793632557687202228')
    case.execute()
    #info_util = Info_Base()
    #bids = info_util.getAllCinemasBid()
    #for i in range(len(bids)):
    #    #print bids[i]
    #    if not bids[i] or bids[i]=='0':
    #        continue
    #    case = Old_Info_Price(bids[i])
    #    case.execute()
