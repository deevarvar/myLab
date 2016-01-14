#-*- coding=utf-8 -*-
'''
@description: 
@author: miliang<miliang@baidu.com>

'''

from settings import MYSQL, ODP_MOVIE_PATH, PHP_BIN, SCRIPT_PATH, SYNC_CINEMAS_SCRIPT, SYNC_GUID_SCRIPT
import os
import MySQLdb
import time

def run(third_from):

    conn = MySQLdb.connect(host=MYSQL['HOST'],port=MYSQL['PORT'],db=MYSQL['DB'],user=MYSQL['USER'],passwd=MYSQL['PASSWD'],charset='utf8')
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    test_cinema_name = 'tc' + str(int(time.time()))

    # 1.获取合作方影院
    cmd = 'cd %s && %s%s %s%s' % (ODP_MOVIE_PATH,ODP_MOVIE_PATH,PHP_BIN,SCRIPT_PATH,SYNC_CINEMAS_SCRIPT)
    os.system(cmd)
	
    # 2.添加自由影院，并关联到第三方影院
    cinemas_columes = []
    cinemas_values = []
    cinemas_columes.append('name')
    cinemas_values.append("'"+test_cinema_name+"'")
    cinemas_columes.append('address')
    cinemas_values.append("'test_address'")
    cinemas_columes.append('phone')
    cinemas_values.append('11111111')
    cinemas_columes.append('city_id')
    cinemas_values.append('131')
    cinemas_columes.append('city')
    cinemas_values.append("'北京市'")
    cinemas_columes.append('area_id')
    cinemas_values.append('1115')
    cinemas_columes.append('area')
    cinemas_values.append("'怀柔区'")
    cinemas_columes.append('point_x')
    cinemas_values.append('11111111')
    cinemas_columes.append('point_y')
    cinemas_values.append('11111111')
    cinemas_columes.append('uid')
    cinemas_values.append('0')
    cinemas_columes.append('status')
    cinemas_values.append('1')
    cinemas_columes.append('publish_status')
    cinemas_values.append('0')
    cinemas_columes.append('publish_feedback')
    cinemas_values.append("' '")
    cinemas_columes.append('brand_id')
    cinemas_values.append('139')
    cinemas_columes.append('brand_name')
    cinemas_values.append("'百老会影城'")
    cinemas_columes.append('shop_begin')
    cinemas_values.append("' '")
    cinemas_columes.append('shop_end')
    cinemas_values.append("' '")
    cinemas_columes.append('introduction')
    cinemas_values.append("' '")
    cinemas_columes.append('traffic')
    cinemas_values.append("' '")
    cinemas_columes.append('imax')
    cinemas_values.append("' '")
    cinemas_columes.append('big_screen')
    cinemas_values.append("' '")
    cinemas_columes.append('3d')
    cinemas_values.append("' '")
    cinemas_columes.append('park')
    cinemas_values.append("' '")
    cinemas_columes.append('love_seat')
    cinemas_values.append("' '")
    cinemas_columes.append('brand_image')
    cinemas_values.append("' '")
    cinemas_columes.append('cinema_image')
    cinemas_values.append("' '")
    cinemas_columes.append('update_time')
    cinemas_values.append('0')
    cinemas_columes.append('support_imax')
    cinemas_values.append('0')
    cinemas_columes.append('relate_update_time')
    cinemas_values.append('0')
    cinemas_columes.append('alias')
    cinemas_values.append("' '")
    cinemas_columes.append('logo')
    cinemas_values.append("' '")
    cinemas_columes.append('province')
    cinemas_values.append("'北京市'")
    cinemas_columes.append('province_id')
    cinemas_values.append('3')
    cinemas_columes.append('biz_area')
    cinemas_values.append("'哈哈哈'")
    cinemas_columes.append('summary')
    cinemas_values.append("' '")
    cinemas_columes.append('notice')
    cinemas_values.append("' '")
    cinemas_columes.append('images')
    cinemas_values.append("'[]'")
    cinemas_columes.append('effect')
    cinemas_values.append("' '")
    cinemas_columes.append('support_2D')
    cinemas_values.append('0')
    cinemas_columes.append('support_3D')
    cinemas_values.append('0')
    cinemas_columes.append('support_double3D')
    cinemas_values.append('0')	
    cinemas_columes.append('support_4D')
    cinemas_values.append('0')
    cinemas_columes.append('support_4DX')
    cinemas_values.append('0')
    cinemas_columes.append('support_4K')
    cinemas_values.append('0')
    cinemas_columes.append('support_reald')
    cinemas_values.append('0')
    cinemas_columes.append('support_jumu')
    cinemas_values.append('0')
    cinemas_columes.append('support_dolby')
    cinemas_values.append('0')
    cinemas_columes.append('support_vip')
    cinemas_values.append('0')
    cinemas_columes.append('support_love_seat')
    cinemas_values.append('0')
    cinemas_columes.append('screen')
    cinemas_values.append("'"+r'{"2D":"","3D":"","Double3D":"","4D":"","4DX":"","4K":"","IMAX":"","Reald":"","Jumu":"","Dolby":"","Vip":""}'+"'")
    cinemas_columes.append('support_pos')
    cinemas_values.append('0')
    cinemas_columes.append('service')
    cinemas_values.append("'"+r'{"glasses":"","qupiaoji":[],"qupiaoji_pos":[],"rest_area":[],"sale":"","wifi":"","love_seat":"","child_ticket":"","vip_card":"","other":""}'+"'")
    cinemas_columes.append('subway')
    cinemas_values.append("'[]'")
    cinemas_columes.append('bus')
    cinemas_values.append("' '")
    cinemas_columes.append('place')
    cinemas_values.append("'"+r'{"cater":"","entertainment":"","shopping":"","park":"","landmark":""}'+"'")
    cinemas_columes.append('review_status')
    cinemas_values.append('0')
    cinemas_columes.append('operator')
    cinemas_values.append("'miliang'")
    cinemas_columes.append('operate_time')
    cinemas_values.append("'2015-03-19 14:06:30'")	
    cinemas_columes_string = ','.join(cinemas_columes)
    cinemas_values_string = ','.join(cinemas_values)
    sql = 'insert into t_movie_cinemas (%s) values (%s)' % (cinemas_columes_string,cinemas_values_string)
    cursor.execute(sql)
    conn.commit()

    sql = "select * from t_movie_cinemas where name='%s'" % test_cinema_name
    cursor.execute(sql)
    test_cinema = cursor.fetchall()[0]

    sql = "select * from t_movie_poi where third_from='%s' limit 0,1" % third_from
    cursor.execute(sql)
    poi_third_cinema = cursor.fetchall()[0]

    sql = "update t_movie_poi set cinemas_id = %s where third_from='%s' and third_id='%s'" % (test_cinema['cinemas_id'],third_from,poi_third_cinema['third_id'])
    cursor.execute(sql)
    conn.commit()
    
    # 3. 同步GUID信息
    cmd = 'cd %s && %s%s %s%s' % (ODP_MOVIE_PATH,ODP_MOVIE_PATH,PHP_BIN,SCRIPT_PATH,SYNC_GUID_SCRIPT)
    os.system(cmd)

    # 4. 配置短信模版
    sms_template = '{A}{B}{C}{D}{E}{F}{G}{H}{I}{J}{K}{L}{M}{N}{O}{P}{Q}{R}{S}{T}{U}{V}{W}{X}{Y}{Z}'
    sms_name = 'test_sms_template'
    sms_mode = '1'
    sql = "insert into t_movie_sms_template (template,name,mode) values ('%s','%s',%s)" % (sms_template,sms_name,sms_mode)
    cursor.execute(sql)
    conn.commit()
    sql = "select * from t_movie_sms_template where name='%s'" % sms_name
    cursor.execute(sql)
    test_sms_template = cursor.fetchall()[0]

    sql = "insert into t_movie_sms_cinema (third_id,third_from,template_id) values(%s,'%s',%s)" % (poi_third_cinema['third_id'],third_from,test_sms_template['template_id'])
    cursor.execute(sql)
    conn.commit()

    # 5. 新建合同、设置服务费
    test_pact_name = 'pact' + str(int(time.time()))
    test_pact_code = test_pact_name
    valid_start_time = '1400000000'
    valid_end_time = '2000000000'
    create_time = int(time.time())
    update_time = create_time
    create_user = 'miliang'
    update_user = create_user
    status = '1'
    sql = "insert into t_movie_pact (code,name,valid_start_time,valid_end_time,create_time,update_time,create_user,update_user,status) values('%s','%s',%s,%s,%s,%s,'%s','%s',%s)" % (test_pact_code,test_pact_name,valid_start_time,valid_end_time,create_time,update_time,create_user,update_user,status)
    cursor.execute(sql)
    conn.commit()

    sql = "select * from t_movie_pact where name='%s'" % test_pact_name
    cursor.execute(sql)
    test_pact = cursor.fetchall()[0]

    # 将影院添加到合同
    sql = "insert into t_movie_pact_cinemas (pact_id,third_id,third_from,status) values(%s,'%s','%s',%s)" % (test_pact['id'],poi_third_cinema['third_id'],third_from,'1')
    cursor.execute(sql)
    conn.commit()


    sql = "select * from t_movie_pact_cinemas where pact_id=%s" % test_pact['id']
    cursor.execute(sql)
    test_pact_cinemas = cursor.fetchall()[0]

    # 服务费
    sql = "insert into t_movie_cinemas_fee (pcid,fee_name,fee_type,fee_value,update_time,update_user,create_time,create_user) values(%s,'接口服务费',2,1,%s,'miliang',%s,'miliang')" % (test_pact_cinemas['id'],int(time.time()),int(time.time()))
    cursor.execute(sql)
    sql = "insert into t_movie_cinemas_fee (pcid,fee_name,fee_type,fee_value,update_time,update_user,create_time,create_user) values(%s,'影院服务费',3,1,%s,'miliang',%s,'miliang')" % (test_pact_cinemas['id'],int(time.time()),int(time.time()))
    cursor.execute(sql)
    sql = "insert into t_movie_cinemas_fee (pcid,fee_name,fee_type,fee_value,update_time,update_user,create_time,create_user) values(%s,'糯米服务费',3,1,%s,'miliang',%s,'miliang')" % (test_pact_cinemas['id'],int(time.time()),int(time.time()))
    cursor.execute(sql)
    conn.commit()

    # 6. 配置结算规则
    status = '1'
    weekday_start = '1'
    weekday_end = '0'
    start_time = '00:00'
    end_time = '23:59'
    rule_type = '1'
    fix_price = '1'
    price_percent = '10000'
    price_add = '1'
    price_min = '1'
    create_user = 'miliang'
    create_time = int(time.time())
    update_user = create_user
    update_time = create_time

    sql = "insert into t_movie_price_rule (pcid,status,weekday_start,weekday_end,start_time,end_time,rule_type,fix_price,price_percent,price_add,price_min,create_user,create_time,update_user,update_time,rule_target_type,huodong_start,huodong_end) values(%s,%s,%s,%s,'%s','%s',%s,%s,%s,%s,%s,'%s',%s,'%s',%s,0,0,0)" % (test_pact_cinemas['id'],status,weekday_start,weekday_end,start_time,end_time,rule_type,fix_price,price_percent,price_add,price_min,create_user,create_time,update_user,update_time)
    cursor.execute(sql)
    conn.commit()

    sql = "select * from t_movie_price_rule where pcid=%s" % test_pact_cinemas['id']
    cursor.execute(sql)
    test_price_rule = cursor.fetchall()[0]

    #配置影片类型结算规则
    for i in range(8):
        sql = "insert into t_movie_price_rule_movie_type (rule_id,type_id) values(%s,%s)" % (test_price_rule['id'],i+1)
        cursor.execute(sql)
        conn.commit()

    #配置影厅结算规则
    sql = "select * from t_movie_third_theater where third_from='%s' and third_id ='%s'" % (third_from,poi_third_cinema['third_id'])
    cursor.execute(sql)
    third_theaters = cursor.fetchall()
    for i in range(len(third_theaters)):
        sql = "insert into t_movie_price_rule_theater (rule_id,t_id) values(%s,%s)" % (test_price_rule['id'],third_theaters[i]['id'])
        cursor.execute(sql)
        conn.commit()





if __name__ == '__main__':
    run('1905')
