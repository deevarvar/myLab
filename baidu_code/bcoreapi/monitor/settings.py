# -*- coding: UTF-8 -*-

'''
# odp_movie模块测试地址
SERVER = {
    'HOST' : '10.94.34.23',
    'PORT' : '8204'
    #'HOST' : 'yf-orp-app0003.yf01',
    #'PORT' : '8240'
}

#Pal模块测试地址
ODP_PAL_SERVER = {
    'HOST' : '10.94.34.23',
    'PORT' : '8888'
}
'''

# 存储模式：1是redis模式，0是本地文件模式
MODE = 1

# 电影测试库配置
MYSQL = {
    'HOST' : '10.94.34.24',
    'PORT' : 3306,
    'DB' : 'instant_info_dq',
    'USER' : 'root',
    'PASSWD' : 'root'
}

# redis配置
REDIS_CONF = {
    'HOST' : '10.94.34.23',
    'PORT' : 8989,
    'DB' : 0,
    'SEQ_DATA_Q' : 'seq_data_q',
    'CINEMA_SEQ_Q' : 'cinema_seq_q',
    'CINEMA_XPT_Q' : 'cinema_xpt_q',
    'ALL_SEQ_SET' : 'all_seq_set',
    'SUC_NO' : 'sec_no',
    'FAIL_NO' : 'fail_no',
    'SEQ_XPT_Q' : {
        'SEAT_INFO' : ('lock_seat_xpt_q','Error Seq Information'),
        'LOCK_SEAT' : ('lock_seat_xpt_q','Error Seq Information')
        }
}

# 新接口支持的合作方列表
PARTNERS = ['wangpiao','maizuo','spider','komovie','shiguang','jinyi','fire','cmts','lanhai','dingxin','xingmei','txpc','vista','cfc','newvista']

# 场次信息文件
SEQ_INFO_FILE = 'seq_info'

# 异常场次文件
EXCEPTION_SEQ_FILES = {
    'SEAT_INFO' : 'si_error.ex',
    'LOCK_SEAT' : 'ls_error.ex'
}

#发送邮件相关
MAIL_LIST = ["miliang"]
MAIL_HOST = "smtp.163.com"
#MAIL_USER = "dnkm001"   #用户名
#MAIL_PASS = "comeon"   #口令
MAIL_USER = "miliangjob"   #用户名
MAIL_PASS = "godreverser"   #口令
MAIL_POSTFIX = "163.com"  #发件箱的后缀

# 各合作方进程数,一个进程里有10个线程,暂且无用
PARTNERS_THREAD_NUM = {
    'wangpiao' : 2,
    'cmts' : 1,
    'dingxin' : 1,
    'fire' : 1,
    'jinyi' : 0,
    'komovie' : 0,
    'lanhai' : 0,
    'maizuo' : 0,
    'shiguang' : 1,
    'spider' : 1,
    'txpc' : 1,
    'vista' : 1,
    'xingmei' : 1,
    'cfc' : 1
}

# 影院id最大值，遍历影院时用到
MAX_CINEMA_ID = 9000
