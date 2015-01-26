#!/bin/bash
# used to stress test xingmei's data interface



#curl -s -o /dev/null -w "@csv.txt" "http://114.215.130.32:9094/xingmei_web/server?cinemaId=112&hallNo=201&uid=baidumovie&method=getSeatsByCinemaAndHall&time_stamp=1421821303155&enc=5e94be5592c7d64723aa787f4c372075"
#curl -s  -w'@csv.txt' "http://114.215.130.32:9094/xingmei_web/server?method=getHallsByCinemaId&cinemaId=101&time_stamp=142182186289&enc=43a55df78f354c80c2fa3b7441a8c7ba&uid=baidumovie"
#curl -s -o /dev/null -w "@csv.txt" "http://114.215.130.32:9094/xingmei_web/server?planId=1421824200000011201&uid=baidumovie&method=getSoldSeats&time_stamp=1421821303270&enc=fd477980d55f48432dcb71adc500a38b"

#curl -s -o /dev/null -w "http://114.215.130.32:9094/xingmei_web/server?uid=baidumovie&method=getCinemas&time_stamp=142182186289&enc=3802937fd2c09019a1ae500710af7d59"
#curl -s -o /dev/null -w "@csv.txt" "http://114.215.130.32:9094/xingmei_web/server?cinemaId=100&uid=baidumovie&method=getPlans&time_stamp=1420451865516&enc=2e2a5349b255c4066fe70dc5f9f0ca85"

#const variable
OFFLINE_DATASERV="http://114.215.130.32:9094/xingmei_web/server"
ONLINE_DATASERV="http://121.40.54.147:9090/xingmei_web/server"
OUTPUTDIR="./output"_$(date +%Y%m%d%H%M%S)
RESULTDIR="./result"_$(date +%Y%m%d%H%M%S)
OUTPUTPREFIX="output"
RESULTPREFIX="result"
USER="baidumovie"
PASSWORD="mxj7hNcRDN2rwcrA"
DATASERVER=${ONLINE_DATASERV}


mkdir -p $OUTPUTDIR
mkdir -p $RESULTDIR

if [ $# -eq 0 ];then

    echo "please input thread number"
    exit -1
fi

thread=$1
for((i=0;i<$1;i++))
do
    curl -s -o $OUTPUTDIR/"$OUTPUTPREFIX"_$i -w "@csv.txt" "$DATASERVER?cinemaId=100&uid=$USER&method=getPlans&time_stamp=1420451865516&enc=2e2a5349b255c4066fe70dc5f9f0ca85" > $RESULTDIR/"$RESULTPREFIX"_$i&
done

wait
echo "thread loop done, start to analyze the data."

#cat ./* >total && cat total |awk -F ',' '{printf "http_code,%s,time_connect,%s,time_total,%s\n",$2,$14,$18}'






