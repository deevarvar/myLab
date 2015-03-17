#!/bin/bash
#add temp solution

dir=/home/work/user/yezhihua/svn/yezhihua/xingmei/data_api/price/
cd ${dir}
time ${dir}/checkPrice.sh |tee ${dir}/log.txt
bash ${dir}/statistics.sh
planflag=$(cat ${dir}/badplanflag)
linenum=$(wc -l ${dir}/wrongprice.csv|cut -d ' ' -f 1)
echo wrongprice num is $linenum, planflag is $planflag
if [ -f ${dir}/wrongprice.csv ] && [ -f ${dir}/xingmei_monitor.html ];then
	#convert to gbk
	if [ $linenum -gt 1 ] || [ $planflag -eq 1 ];then

		attachstring=" -a ${dir}/log.txt "
		if [ $linenum -gt 1 ];then
			cat ${dir}/wrongprice.csv |iconv -f utf8 -t gb2312 > ${dir}/wrong.csv
			attachstring=$attachstring" -a ${dir}/wrong.csv"
		fi

		cat ${dir}/xingmei_monitor.html |/home/work/.jumbo/bin/mutt -s "xingmei monitor" -b xpandxx@126.com -c bmovie-qa@baidu.com -c xiongbing@baidu.com -c huangjie@smimovie.com -e "my_hdr From:yezhihua@baidu.com" -e "set content_type=text/html" $attachstring -- yezhihua@baidu.com chengweiguang@baidu.com yaopengyan@baidu.com qiaoyi@baidu.com pengxingbang@baidu.com liangkaichun@baidu.com fanjiadong@smimovie.com xuwei@smimovie.com lijuanyy@smimovie.com liugejt@smimovie.com 
		#cat ${dir}/xingmei_monitor.html |/home/work/.jumbo/bin/mutt -s "xingmei monitor" -e "my_hdr From:yezhihua@baidu.com" -e "set content_type=text/html" $attachstring  -- yezhihua@baidu.com 

	else	
#		: > ok
#		echo "all xingmei price are right" >> ok 
#		ls -lR ${dir}/raw|sort -k 5 -n >> ok
		bash ${dir}/statistics.sh showall.html
		cat ${dir}/planstat.csv |iconv -f utf8 -t gb2312 > ${dir}/plan.csv
		cat ${dir}/badplan.csv |iconv -f utf8 -t gb2312 > ${dir}/bad.csv
		cat ${dir}/showall.html | /home/work/.jumbo/bin/mutt -s 'xingmei monitor ok' -e "my_hdr From:yezhihua@baidu.com" -e "set content_type=text/html" -a ${dir}/bad.csv -a ${dir}/plan.csv -- yezhihua@baidu.com xpandxx@126.com
	fi
else
	echo "no price is generated,check log" | mutt -s "xingmei monitor error" -a ${dir}/log.txt -a ${dir}/pricecron.log-- yezhihua@baidu.com

fi



