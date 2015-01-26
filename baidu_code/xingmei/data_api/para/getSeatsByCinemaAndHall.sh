#!/bin/bash

#echo $0 thread No.$1

OUTPUTPREFIX="output"
RESULTPREFIX="result"
OUTPUT=${OUTPUTPREFIX}_$1
RESULT=${RESULTPREFIX}_$1


SERVER="http://121.40.54.147:9090/xingmei_web/server"

curl -s -o $OUTPUT -w "@csv.txt" "$SERVER?cinemaId=112&hallNo=201&uid=baidumovie&method=getSeatsByCinemaAndHall&time_stamp=1421821303155&enc=5e94be5592c7d64723aa787f4c372075" > $RESULT
