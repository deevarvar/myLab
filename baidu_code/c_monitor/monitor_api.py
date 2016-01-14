#!/usr/bin/env python
#-*- coding=utf-8 -*-
#author: yezhihua@baidu.com

import urllib,urllib2,json
import queue_monitor

def input_monitor_plat(item_id, value, content):
	try:
		data = {"item_id":item_id, "value": value, "content":content}
		body = urllib.urlencode(data)
		fp = urllib2.urlopen("http://cq02-testing-mb13.cq02.baidu.com:8282/movie_monitor/alarm_storage?"+body)
		res_str = fp.readlines()
		json_str = json.loads(res_str[0])
		if "OK" == json_str[0]["message"]:
			print "succeed!"
		else:
			print "failed!"
	except Exception, e:
		err_msg = "Exception in api: %s!"%e
		print err_msg

if __name__ == '__main__':
    result = queue_monitor.queue_monitor().getPage()
    print "result is "+str(result)
    result["schedulequeue"]['num'] = 200
    result["adjust"]['num'] = 200
    result["record"]['num'] = 200
    alarm_queue = ''
    alarm_flag = 0
for key in result:
    value = result[key]
    if int(value['num']) > int(value['level']):
        alarm_flag = 1
        alarm_queue += value['name'] + '(' + str(value['num']) +  '>' + str(value['level']) + ')  '

if alarm_flag == 1:
    monitor_item_id = 49
    alarm_value = 1
    alarm_content = "MQ_SERVER队列长度超过阈值! " + alarm_queue
    print alarm_content
    #input_monitor_plat(monitor_item_id, alarm_value, alarm_content)
