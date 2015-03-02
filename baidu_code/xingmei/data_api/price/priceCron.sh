#!/bin/bash
#add temp solution

dir=/home/work/user/yezhihua/svn/yezhihua/xingmei/data_api/price/
cd ${dir}
time ${dir}/checkPrice.sh |tee ${dir}/log.txt
bash ${dir}/statistics.sh

linenum=$(wc -l ${dir}/wrongprice.csv|cut -d ' ' -f 1)
echo linenum is $linenum
if [ -f ${dir}/wrongprice.csv ] && [ -f ${dir}/xingmei_monitor.html ];then
	#convert to gbk
	if [ $linenum -gt 1 ];then
	cat ${dir}/wrongprice.csv |iconv -f utf8 -t gb2312 > ${dir}/wrong.csv
	cat ${dir}/xingmei_monitor.html |/home/work/.jumbo/bin/mutt -s "xingmei price monitor" -b xpandxx@126.com -c bmovie-qa@baidu.com -c xiongbing@baidu.com -e "my_hdr From:yezhihua@baidu.com" -e "set content_type=text/html" -a ${dir}/wrong.csv -a ${dir}/log.txt -- yezhihua@baidu.com chengweiguang@baidu.com yaopengyan@baidu.com fanjiadong@smimovie.com xuwei@smimovie.com lijuanyy@smimovie.com  
	#cat ${dir}/xingmei_monitor.html |/home/work/.jumbo/bin/mutt -s "xingmei price monitor" -e "my_hdr From:yezhihua@baidu.com" -e "set content_type=text/html" -a ${dir}/wrong.csv -a ${dir}/log.txt -- yezhihua@baidu.com 

	else	
		: > ok
		echo "all xingmei price are right" >> ok 
		ls -lR ${dir}/raw|sort -k 5 -n >> ok
		cat ok | /home/work/.jumbo/bin/mutt -s 'xingmei price monitor ok' -e "my_hdr From:yezhihua@baidu.com"  -- yezhihua@baidu.com xpandxx@126.com
	fi
else
	echo "no price is generated,check log" | mutt -s "xingmei price monitor error" -a ${dir}/log.txt -a ${dir}/pricecron.log-- yezhihua@baidu.com

fi



