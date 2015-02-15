#!/bin/bash
dir=/home/work/user/yezhihua/svn/yezhihua/xingmei/data_api/price/
cd ${dir}
time ${dir}/checkPrice.sh |tee ${dir}/log.txt
bash ${dir}/statistics.sh
if [ -f ${dir}/wrongprice.csv ] && [ -f ${dir}/xingmei_monitor.html ];then
	#convert to gbk
 	cat ${dir}/wrongprice.csv |iconv -f utf8 -t gb2312 > ${dir}/wrong.csv
	cat ${dir}/xingmei_monitor.html |/home/work/.jumbo/bin/mutt -s "xingmei price monitor" -c bmovie-qa@baidu.com -c xiongbing@baidu.com -e "my_hdr From:yezhihua@baidu.com" -e "set content_type=text/html" -a ${dir}/wrong.csv -a ${dir}/log.txt -- yezhihua@baidu.com chengweiguang@baidu.com yaopengyan@baidu.com 
else
	echo "no price is generated,check log" | mutt -s "xingmei price monitor error" -a ${dir}/log.txt -a ${dir}/pricecron.log-- yezhihua@baidu.com

fi


