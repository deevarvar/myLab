#!/bin/bash
#use xargs, not parallel

if [ $# -ne 3 ];then

    echo "please input thread_num max_concurrent_num and script"
    echo "usage: $0 thread_num max_concurrent_num script_name."
    exit 1
fi




TIMESTAMP=$(date +%Y%m%d%H%M%S)
JOBNAME=$(basename `readlink -f $3`| cut -d . -f 1)
RUNDIR="./${JOBNAME}_run"_${TIMESTAMP}_$$

#echo arguments are $1 $2 $3

mkdir -p $RUNDIR
cp $3 $RUNDIR
cp ./csv.txt $RUNDIR
cd $RUNDIR

start=$(date +%s)
seq $1|xargs -n 1 -P $2 ./$3

# dig log
cat result_* |awk -F ',' '{printf "http_code,%s,time_connect,%s,time_total,%s\n",$2,$14,$18}' > trim_result

#http status code
httpok=$(cat trim_result | awk -F ',' '$2=200' |wc -l)
httprate=$(echo ${httpok}/$1*100|bc -l)



analyze_time(){
  min=$(cat trim_result |sort -n -t ,|awk -F , '{print $'$1'}' |head -n 1)
  max=$(cat trim_result |sort -n -t ,|awk -F , '{print $'$1'}' |tail -n 1)
  avg=$(cat trim_result |awk -F , '{ sum +=sprintf("%f",$'$1')} END { if (NR > 0) printf "%f",sum/NR}')
  echo "最小${2}s,最大${2}s,平均${2}s"
  echo $min,$max,$avg
}

#time connect find the min, max, average
#connectindex=4
#analyze_time $connectindex "ConnectTime"

#time_total， find the min,max,average
totalindex=6
end=$(date +%s)
duration=$(($end-$start))
echo "并发数 $2 压力测试时间 ${duration}s"
#default locale is UTF-8, should convert to gb2312
echo "Http状态返回200比率,${httprate:0:6}%"
analyze_time $totalindex "响应时间"

cd - >/dev/null
