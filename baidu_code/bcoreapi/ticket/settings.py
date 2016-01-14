ODP_MOVIE_PATH = '/home/map/odp_movie'

OLD_PARTNER_SUPPORTED = ['cmts','dingxin','jinyi','maizuo','txpc','vista','newvista','wangpiao','cfc']
# new api ignoring : komovie,lanhai
NEW_PARTNER_SUPPORTED = ['cmts','dingxin','fire','jinyi','shiguang','maizuo','spider','txpc','vista','wangpiao','xingmei','cfc']

SERVER = {
    # pool04    
    'HOST' : '10.94.34.26',
    'PORT' : '8204'

    # online
    #'HOST' : 'yf-orp-app0003.yf01',
    #'PORT' : '8240'

    # yangyu's odp_movie
    #'HOST' : '10.94.22.20',
    #'PORT' : '8111'
}

ODP_PAL_SERVER = {
    # pool04
    'HOST' : '10.94.34.26',
    'PORT' : '8888'

    # yangyu's odp_pal
    #'HOST' : 'cp01-ocean-pool002.cp01.baidu.com',
    #'PORT' : '8888'
}

REDIS_CONF = {
    'HOST' : '10.94.34.26',
    'PORT' : 6379,
    'DB' : 0,
    'SUC_NO' : 'sec_no',
    'FAIL_NO' : 'fail_no'
}

MYSQL = {
    # pool03
    'HOST' : '10.94.34.26',
    'PORT' : 3305,
    'DB' : 'instant_info',

    # yangyu's sql
    #'HOST' : '10.58.102.38',
    #'PORT' : 3306,
    #'DB' : 'instant_info',

    'USER' : 'root',
    'PASSWD' : 'root'
}

#SIGN_KEY = 'seat'
SIGN_KEY = 'b_movie_core_api'
#SIGN_KEY = 'B_MOVIE_CORE_API'
ONLINE_SIGN_KEY = 'b_movie_core_api'
PAGE_SIGN_KEY = 'baidu'
#PAY_NOTICE_SIGN_KEY = '8343e400f6b0ff2fc13337f7f2cf33ff'
PAY_NOTICE_SIGN_KEY = '123456'
