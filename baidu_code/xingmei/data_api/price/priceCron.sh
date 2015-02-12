#!/bin/bash
time ./checkPrice.sh |tee log

if [ -f wrongprice.csv ];then
	#convert to gbk
 	cat wrongprice.csv |iconv -f utf8 -t gb2312 > wrong.csv
	echo "the result is in the attachment" |mutt -s "xingmei price monitor" -a wrong.csv log -- yezhihua@baidu.com
else
	echo "no price is generated,check log"| mutt -s "xingmei price monitor error" -a log -- yezhihua@baidu.com

fi
