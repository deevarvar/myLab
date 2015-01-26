#!/bin/bash

#echo $0 thread No.$1

OUTPUTPREFIX="output"
RESULTPREFIX="result"
OUTPUT=${OUTPUTPREFIX}_$1
RESULT=${RESULTPREFIX}_$1


SERVER="http://121.40.54.147:9090/xingmei_web/server"

curl -s -o $OUTPUT -w "@csv.txt" "$SERVER?method=getHallsByCinemaId&cinemaId=101&time_stamp=142182186289&enc=43a55df78f354c80c2fa3b7441a8c7ba&uid=baidumovie" > $RESULT
