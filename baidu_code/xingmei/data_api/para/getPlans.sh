#!/bin/bash

#echo $0 thread No.$1

OUTPUTPREFIX="output"
RESULTPREFIX="result"
OUTPUT=${OUTPUTPREFIX}_$1
RESULT=${RESULTPREFIX}_$1


SERVER="http://121.40.54.147:9090/xingmei_web/server"

curl -s -o $OUTPUT -w "@csv.txt" "$SERVER?cinemaId=100&uid=baidumovie&method=getPlans&time_stamp=1420451865516&enc=2e2a5349b255c4066fe70dc5f9f0ca85" > $RESULT
