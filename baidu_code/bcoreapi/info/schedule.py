#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——排期接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Info_Schedule(Info_Base):
    def __init__(self,cinema_id=None,encode_bid=None,bid=None):
        super(Info_Schedule,self).__init__()
        self.req_url = self.req_url + 'schedule'
        self.req_dict = {}
        if cinema_id:
            self.req_dict['cinema_id'] = cinema_id
            self.cinema_id = cinema_id
        if encode_bid:
            self.req_dict['encode_id'] = encode_id
            self.encode_id = encode_id
        if bid:
            self.req_dict['bid'] = bid
            self.bid = bid

    def doAssert(self):
        print self.page_dict
        assert self.page_dict['errorMsg'] == 'Success'
        assert self.page_dict['movie_id']
        assert self.page_dict['time_table']
        partner = ''
        for date in self.page_dict['time_table']:
            for schedule in self.page_dict['time_table'][date]:
                #上一个合作方的竞争价，要求按竞争价升序排列(下线了)
                #former_com_price = 0
                assert schedule['time']
                assert schedule['date']
                assert schedule['movie_id']
                assert schedule['end_time']
                assert schedule.has_key('src_info')
                for i in range(len(schedule['src_info'])):
                    assert schedule['src_info'][i]['src']
                    # 5.11:仅返回C端同一合作方的影讯
                    if partner == '':
                        partner = schedule['src_info'][i]['src']
                    else :
                        assert schedule['src_info'][i]['src'] == partner

                    assert schedule['src_info'][i].has_key('lan') # 这个暂时可能为空
                    assert schedule['src_info'][i].has_key('type') # 这个暂时可能为空
                    assert schedule['src_info'][i]['origin_price']
                    assert schedule['src_info'][i]['price']
                    assert schedule['src_info'][i].has_key('seq_no') # 这个暂时可能为空
                    assert schedule['src_info'][i]['third_cinema_id']
                    assert schedule['src_info'][i]['third_movie_id']
                    assert schedule['src_info'][i]['theater']
                    assert schedule['src_info'][i]['src_name']
                    assert schedule['src_info'][i]['out_buy_time'] 
                    assert schedule['src_info'][i].has_key('hall_id')    # 这个暂时可能为空
                    assert schedule['src_info'][i].has_key('weight')
                    assert schedule['src_info'][i].has_key('status') and schedule['src_info'][i]['status'] == 0 or schedule['src_info'][i]['status'] == 1
                    #assert schedule['src_info'][i].has_key('com_price') and schedule['src_info'][i]['com_price'] >= former_com_price
                    #former_com_price = schedule['src_info'][i]['com_price']



if __name__ == '__main__':
     
    case = Info_Schedule(cinema_id=8350)
    case.execute()
