#-*- coding=utf-8 -*-
'''
@description: 影讯新接口——影院禁售规则渠道接口测试用例。
@author: miliang<miliang@baidu.com>

'''

from base import Info_Base

class Info_Cinema_Sfrom_Rule(Info_Base):
    def __init__(self,cinema_id,forbiden=0,third=None,channel=None):
        super(Info_Cinema_Sfrom_Rule,self).__init__()
        self.req_url = self.req_url + 'sfromrule'
        self.req_dict = {"cinema_id":cinema_id}
        self.cinema_id = cinema_id
        self.forbiden = forbiden
        self.third = third
        self.channel = channel

    def doAssert(self):
        #print self.page_dict['errorMsg']
        assert self.page_dict['errorMsg'] == 'Success'
        assert self.page_dict.has_key('data')
        # 在mis配置了一条spider在newnuomi的禁售规则，并添加了cinema_id=344为例外。
        if self.forbiden == 0:
        # 未设置禁售规则或例外影院
            assert len(self.page_dict['data'][self.third]) == 0
        else:
        # 影院在禁售规则内
            assert self.channel in self.page_dict['data'][self.third]
        

if __name__ == '__main__':

    # 在mis配置了一条spider在newnuomi的禁售规则，并添加了cinema_id=344为例外。
    case = Info_Cinema_Sfrom_Rule(1,forbiden=1,third='spider',channel='newnuomi')
    case.execute()
    case = Info_Cinema_Sfrom_Rule(344,forbiden=0,third='spider',channel='newnuomi')
    case.execute()
