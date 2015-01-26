#!/bin/bash


#run the excel once

scripts_array=(getCinemas getHallsByCinemaId getPlans getSeatsByCinemaAndHall getSoldSeats)

#three args: total times, cocurrent num, script name
run_parallel(){
./parallel.sh $1 $2 $3
}

TIMESTAMP=$(date +%Y%m%d%H%M%S)


run_batch(){
echo $1 1500/10
run_parallel 1500 10 $1.sh > $1_${TIMESTAMP}.csv
sleep 2 && echo $1 1500/20
run_parallel 1500 20 $1.sh >>  $1_${TIMESTAMP}.csv
sleep 2 && echo $1 1500/50
run_parallel 1500 50 $1.sh >>  $1_${TIMESTAMP}.csv
sleep 2 && echo $1 1500/80
run_parallel 1500 80 $1.sh >>  $1_${TIMESTAMP}.csv
sleep 2 &&  echo $1 1500/100
run_parallel 1500 100 $1.sh >>  $1_${TIMESTAMP}.csv

#seems default excel only recog the gb2312

cat $1.csv|iconv -f utf-8 -t gb2312 > /mnt/hgfs/Project/$1_${TIMESTAMP}.csv
}


#run_batch getPlans

for((i=0; i<${#scripts_array[*]};i++))
do

    run_batch ${scripts_array[i]}

done

