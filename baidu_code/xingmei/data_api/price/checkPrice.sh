#!/bin/bash
#todo: use python to rewrite...
#1. generate checksum
#2. get plan
#3. city  time

FIRSTCITIES=(100 101 102 105 128 138 139 140 143 144 149 163 166 167 174)
SECONDCITIES=(104 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 129 130 131 132 133 134 135 136 137 141 145 146 147 148 150 151 152 154 156 157 158 159 160 161 162 164 165 168 169 170 171 172 173 175 176 177 178)
SPECIALCITIES=(103 142 155 153)
SERVER="http://182.92.217.248:8090/xingmei_web/server"
uid=baidumovie
passwd="O1wBNQgxOBvjgrBJ"
timestamp=$(date +%s)
cinemaId=""
method=getPlans





#
#planword="planInfo"
#timeword="starttime"

#marketPrice="marketPrice"
#price="price"

#todo: use json to format data
#price rule
workdays=(1 2 3 4 5)
restdays=(0 6)

duration_first_work="02:00,17:15"
price_rule_first_work="30,0.6"
duration_second_work="02:00,17:15"
price_rule_second_work="25,0.6"
duration_special_work="02:00,17:15"
price_rule_special_work="30,0.7"


duration_first_rest="02:00,12:00"
price_rule_first_rest="30,0.6"
duration_second_rest="02:00,12:00"
price_rule_second_rest="25,0.6"
duration_special_rest="02:00,12:00"
price_rule_special_rest="30,0.7"


mkdir -p raw
mkdir -p format

echo "城市,影院id, 影厅id,场次号,开始时间,周几,marketPrice,price,理论价" > "./wrongprice.csv"

containsElement () {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 1; done
  return 0
}

#arguments: cinemaId, prefix, timeString,marketPrice,price,planId, hallId
processPrice(){
    cinemaId=$1
    prefix=$2
    timeString=$3
    marketPrice=$4
    price=$5
    planId=$6
    hallId=$7

    starttime=$(echo $timeString|cut -d '"' -f 2)
    startday=$(echo $starttime|cut -d ' ' -f 1)
    weekday=$(date -d "$startday" +%w)
    startsec=$(date -d "$starttime" +%s)

    #echo $1,$2,$3,$4,$5,$6,$7
    # calculate the price
    postfix="work"
    containsElement "$weekday" "${restdays[@]}"
    if [ $? -eq 1 ];then
        postfix="rest"
    fi

    duration="duration_${prefix}_${postfix}"
    price_rule="price_rule_${prefix}_${postfix}"

    default_price=$(eval echo \$${price_rule}| cut -d , -f 1)
    discount=$(eval echo \$${price_rule}|cut -d , -f 2)



    #echo default price is ${default_price}, discount is ${discount}

    #compare time
    #unify to seconds
    duration_start="$startday "$(eval echo \$$duration|cut -d , -f 1)
    duration_end="$startday "$(eval echo \$$duration|cut -d , -f 2)
    echo start:${duration_start}, end: ${duration_end}
    stdstart=$(date -d "${duration_start}" +%s)
    stdend=$(date -d "${duration_end}" +%s)

 echo "city type:$prefix, cinema: $cinemaId, hallId: $hallId, plan $planId, time is $starttime, weekday is $weekday, marketPrice is $marketPrice"
    if [ ${startsec} -ge ${stdstart} ] && [ ${startsec} -le ${stdend} ];then

       targetPrice=$default_price
       echo default :$targetPrice, $price
    else
        targetPrice=$(echo $marketPrice $discount | awk '{printf "%.1f", $1*$2 }')
        echo discoutn: $targetPrice, $price
    fi

    result=$(echo $targetPrice $price|awk '{printf "%f", $1-$2}')
    result=$(echo $result-0|bc)

    if [ $result != 0 ];then
        echo "$prefix,$cinemaId,$hallId,$planId,$starttime,$weekday,$marketPrice,$price,$targetPrice" >> "./wrongprice.csv"
    fi

}
#two arguments: cinemaId, file_prefix
processPlans(){
    cinemeId=$1
    prefix=$2
    enc=$(echo -n ${cinemaId}${method}${timestamp}${uid}${passwd}|md5sum|cut -d ' ' -f 1)
    requrl="$SERVER?cinemaId=${cinemaId}&method=${method}&time_stamp=${timestamp}&uid=${uid}&enc=${enc}"
    curl  "${requrl}" -o temp
    rawfile="raw/${prefix}_${cinemaId}.json"
    formatfile="format/${prefix}_${cinemaId}.format"


    cat temp|python -mjson.tool > ${rawfile}
    cat $rawfile|./JSON.sh > ${formatfile}


#data format:
#["data","planInfo",0,"starttime"]       "2015-01-26 11:10:00"
#["data","planInfo",0,"marketPrice"]     120.0

#get plan num
planNum=$(grep -o "planInfo\",[0-9]\+," $formatfile |uniq|sort -t , -nk2|tail -n 1|cut -d , -f 2)
echo planNum is $planNum

for((index=0;index < planNum;index++))
do
    #get the starttime and weekday
    #echo timeString is $timeString
    #find marketPrice, price, starttime, weekday,qid
    timeString=$(grep "planInfo\",$index,\"starttime\"" $formatfile |cut -f 2)
    marketPrice=$(grep "planInfo\",$index,\"marketPrice\"" $formatfile|cut -f 2)
    price=$(grep "planInfo\",$index,\"price\"" $formatfile|cut -f 2)
    planId=$(grep "planInfo\",$index,\"qid\"" $formatfile|cut -f 2)
    hallId=$(grep "planInfo\",$index,\"hallNo\"" ${formatfile} |cut -f 2|cut -d \" -f 2)

    #double quote is IMPORTANT!!!
    processPrice $cinemaId $prefix "$timeString" $marketPrice $price $planId $hallId
done

}



#use this line to do unit test
# processPrice $1 $2 "$3" $4 $5 $6 $7

#shell blockcomment
: << BLOCKCOMMENT
BLOCKCOMMENT



#first tie cities
for((i=0; i<${#FIRSTCITIES[*]}; i++))
#for((i=0; i<1; i++))
do
    cinemaId=${FIRSTCITIES[i]}
    processPlans $cinemaId "first"

done




#second tie cities
for((i=0; i<${#SECONDCITIES[*]}; i++))
#for((i=0; i<1; i++))
do
    cinemaId=${SECONDCITIES[i]}
    processPlans $cinemaId "second"
done

#special cities
for((i=0; i<${#SPECIALCITIES[*]}; i++))
#for((i=0; i<1; i++))
do
    cinemaId=${SPECIALCITIES[i]}
    processPlans $cinemaId "special"
done


rm -f temp
