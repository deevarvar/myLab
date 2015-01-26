#!/bin/bash

#echo $0 thread No.$1

OUTPUTPREFIX="output"
RESULTPREFIX="result"
OUTPUT=${OUTPUTPREFIX}_$1
RESULT=${RESULTPREFIX}_$1


SERVER="http://121.40.54.147:9090/xingmei_web/server"

curl -s -o $OUTPUT -w "@csv.txt" "$SERVER?uid=baidumovie&method=getCinemas&time_stamp=142182186289&enc=3802937fd2c09019a1ae500710af7d59" > $RESULT
