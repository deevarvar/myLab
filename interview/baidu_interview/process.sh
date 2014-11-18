#!/bin/bash
OLD_IFS=$IFS
#IFS must be set to empty
#or the space between will be trimmed
: > part.1
: > part.2
: > part.3



IFS=''
while read -r line
do
	echo ---------$line-------
	#first of all we get first part
	partone=`echo $line| cut -d ' ' -f 1`
	echo $partone >> part.1
	echo "partone is $partone"
	len=${#partone}
	remain=${line:$len}
	#second trim possible space
	trim_remain=`echo $remain|sed 's/^ *//'`
	#echo $trim_remain
	#if no space is left, column two is empty, trim_remain is all we had
	flag=`echo $trim_remain|grep ' '`
	if [ -z $flag ]
	then
		echo "parttwo is empty"
		echo >> part.2
		echo "part three is $trim_remain"
		echo $trim_remain >> part.3
	else
		parttwo=`echo $trim_remain|cut -d ' ' -f 1`
		echo "parttwo is $parttwo"
		echo $parttwo >> part.2
		#handle left string
		twolen=${#parttwo}
		last=${trim_remain:$twolen}
		trim_last=`echo $last|sed 's/^ *//'`
		echo "part three is $trim_last"
		echo $trim_last>> part.3
	fi

done < log_temp.txt

IFS=$OLD_IFS
