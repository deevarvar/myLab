#!/bin/bash

#clean result file
: > result.txt
: > final_result.txt
#remove head/tail line, run only once
#sed -i -e '1d' -e '$d' $DIR/*.data

export LC_ALL=en_US.UTF-8

#column number
comment_col=5
reason_col=10


for file in `ls *.data`
do
    echo "---------------$file------------------"
    #the null char is the delimeter
    cat $file | cut -d ''  -f "$comment_col","$reason_col" | tr '\0' '|' >> result.txt
done

#sort and make the reason the first column
sort -t '|' -k2 result.txt | awk -F "|" '{print $2"|"$1}' | tr -d '\r'> final_result.txt

mkdir -p result_dir && cd result_dir
sed -n '/^|/'p ../final_result.txt > noreason.txt
awk -F '|' '$1!="" {print > $1}' ../final_result.txt
