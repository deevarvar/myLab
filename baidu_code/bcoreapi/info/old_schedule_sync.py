#-*- coding=utf-8 -*-
'''
@description: 从第三方拉取影讯的测试用例。
@author: miliang<miliang@baidu.com>

'''

import os
import json
import MySQLdb
from settings import ODP_MOVIE_PATH,MYSQL

class Info_Old_Schdule_Sync(object):
    def __init__(self,third_from):
        self.third_from = third_from
        self.mysql = MySQLdb.connect(host=MYSQL['HOST'],port=MYSQL['PORT'],db=MYSQL['DB'],user=MYSQL['USER'],passwd=MYSQL['PASSWD'])
        self.cursor = self.mysql.cursor()
    
    def execute(self):
        php_bin = ODP_MOVIE_PATH + 'php/bin/php'
        sync_script_path = ODP_MOVIE_PATH + 'app/info/script/'
        sync_script_file = sync_script_path + 'sync' + self.third_from + '.php'
        # 删除原有排期表的内容
        sql = 'delete from t_movie_cache_odp'
        self.cursor.execute(sql)
        self.mysql.commit()
        # 执行拉取影讯的脚本
        cmd = '%s %s' % (php_bin,sync_script_file)
        print cmd
        os.system(cmd)
        # 验证影讯、场次
        self.doAssert()

    def doAssert(self):
        sql = "select * from t_movie_cache_odp where third_from='%s'" % self.third_from.lower()
        self.cursor.execute(sql)
        base_flag = 0
        schedule_flag = 0
        base_check_items = ['movie_name','movie_id','movie_type','movie_nation','movie_director','movie_starring','movie_release_date','movie_picture','movie_length','video_id','works_id','local_movie_id']
        schedule_check_items = ['time','lan','date','origin_price','movie_id','theater','video_id','src_info']
        src_info_check_items = ['src','price','seq_no','movie_id','cinema_id','video_id']
        for sql_result in self.cursor.fetchall():
            cinema = json.loads(sql_result[3])
            if not cinema.has_key('base') or not cinema['base'] or not cinema.has_key('time_table') or not cinema['time_table']:
                continue
            # 影讯部分验证
            for base in cinema['base']:
                if base_flag == 1:
                    break
                base_break_reason = 0
                for item in base_check_items:
                    if not base.has_key(item) or not base[item]:
                        base_break_reason = 1
                        break
                if base_break_reason == 0:
                    base_flag = 1
                    break
            # 场次部分验证
            for date in cinema['time_table']:
                if schedule_flag == 1:
                    break
                for schedule in date:
                    if schedule_flag == 1:
                        break
                    schedule_break_reason = 0
                    for item in schedule_check_items:
                        if not schedule.has_key(item) or not schedule[item]:
                            schedule_break_reason = 1
                            break

                    if schedule_break_reason != 0:
                        continue

                    for src_item in src_info_check_items:
                        if not schedule['src_info'][0].has_key(src_item) or not schedule['src_info'][0][src_item]:
                            schedule_break_reason = 1
                            break
                    if schedule_break_reason == 0:
                        schedule_flag = 1
                        break
                
            if base_flag == 1 and schedule_flag == 1:
                break

        assert base_flag == 1 and schedule_flag == 1
                           

if __name__ == '__main__':
    test = Info_Old_Schdule_Sync('Cfc')
    test.execute()
