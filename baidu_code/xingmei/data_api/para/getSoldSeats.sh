#!/bin/bash

#echo $0 thread No.$1

OUTPUTPREFIX="output"
RESULTPREFIX="result"
OUTPUT=${OUTPUTPREFIX}_$1
RESULT=${RESULTPREFIX}_$1


SERVER="http://121.40.54.147:9090/xingmei_web/server"

curl -s -o $OUTPUT -w "@csv.txt" "$SERVER?planId=1422024600000010017&uid=baidumovie&method=getSoldSeats&time_stamp=1421928228355&enc=63bd72e24931206c071448d58bc5294e"> $RESULT
