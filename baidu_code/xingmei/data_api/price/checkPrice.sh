#!/bin/bash
#author: yezhihua@baidu.com
#todo: use python to rewrite...
#1. generate checksum
#2. get plan
#3. city  time


#add more log check
#0. empty check
#1. cinema statistics
#2. time statistics
#3. html rendering


#add movie type check
#IMAX, DMAX's price is not changed.


dir=$(dirname $0)


FIRSTCITIES=(100 101 102 105 128 138 139 140 143 144 149 163 166 167 174 103 142)
SECONDCITIES=(104 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 129 130 131 132 133 134 135 136 137 141 145 146 147 148 150 151 152 154 156 157 158 159 160 161 162 164 165 168 169 170 171 172 173 175 176 177 178 155 153)
SPECIALCITIES=(103 142 155 153)
SERVER="http://182.92.217.248:8090/xingmei_web/server"
uid=baidumovie
passwd="O1wBNQgxOBvjgrBJ"
timestamp=$(date +%s)
cinemaId=""
planMethod=getPlans
cinemaMethod=getCinemas
cinemaJson=cinema.json

rm -f cinema.*


#
#planword="planInfo"
#timeword="starttime"

#marketPrice="marketPrice"
#price="price"

#todo: use json to format data
#price rule
#进口片8644 和 8610 的一线25 二线20
foreign_movies=(8644 8610 8627)
#霍比特人3：五军之战,坚不可摧,第七子：降魔之战

foreignPrice_first=25
foreignPrice_second=20


workdays=(1 2 3 4 5)
restdays=(0 6)

duration_first_work="02:00,17:15"
duration_second_work="02:00,17:15"
duration_special_work="02:00,17:15"
duration_first_rest="02:00,12:00"
duration_second_rest="02:00,12:00"
duration_special_rest="02:00,12:00"


price_rule_first_work_3D="30,0.6"
price_rule_first_work_2D="25,0.6"
price_rule_second_work_3D="25,0.6"
price_rule_second_work_2D="20,0.6"
price_rule_special_work_3D="30,0.7"
price_rule_special_work_2D="25,0.7"


price_rule_first_rest_3D="30,0.6"
price_rule_first_rest_2D="25,0.6"
price_rule_second_rest_3D="25,0.6"
price_rule_second_rest_2D="20,0.6"
price_rule_special_rest_3D="30,0.7"
price_rule_special_rest_2D="25,0.7"




mkdir -p raw
mkdir -p format

echo "城市,影院id, 影院名,影厅id,movieId,场次号,开始时间,周几,marketPrice,price,理论价,movieType,VIP厅,primetime" > "./wrongprice.csv"



getCinema(){
   enc=$(echo -n ${cinemaMethod}${timestamp}${uid}${passwd}|md5sum|cut -d ' ' -f 1)
   requrl="$SERVER?method=${cinemaMethod}&time_stamp=${timestamp}&uid=${uid}&enc=${enc}"
   curl -s -o ${cinemaJson} $requrl
}


#http://stackoverflow.com/questions/1494178/how-to-define-hash-tables-in-bash
arrayGet() {
    local array=$1 index=$2
    local i="${array}_$index"
    #printf '%s' "${!i}"
    echo -n ${!i}
}


genCinemaPair() {

    getCinema
    cat ${cinemaJson}|${dir}/JSON.sh -l > cinema.format
    grep cinemaId cinema.format | awk '{print $2}' > cinema.id
    grep cinemaName cinema.format | awk '{print $2}'|cut -d '"' -f 2 > cinema.name
    #gen cinema id,name pair, format is : id,name
    paste -d, cinema.id cinema.name > cinema.pair

}




containsElement () {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 1; done
  return 0
}

#arguments: cinemaId, prefix, timeString,marketPrice,price,planId,movieId, movieType
processPrice(){
    cinemaId=$1
    prefix=$2
    timeString=$3
    marketPrice=$4
    price=$5
    planId=$6
    hallId=$7
    movieId=$8
    movieType=$9

    starttime=$(echo $timeString|cut -d '"' -f 2)
    startday=$(echo $starttime|cut -d ' ' -f 1)
    weekday=$(date -d "$startday" +%w)
    startsec=$(date -d "$starttime" +%s)

    #echo $1,$2,$3,$4,$5,$6,$7,$8
    # calculate the price
    postfix="work"
    containsElement "$weekday" "${restdays[@]}"
    if [ $? -eq 1 ];then
        postfix="rest"
    fi

    duration="duration_${prefix}_${postfix}"
    price_rule="price_rule_${prefix}_${postfix}_${movieType}"

    default_price=$(eval echo \$${price_rule}| cut -d , -f 1)


    #echo default price is ${default_price}, discount is ${discount}

    #compare time
    #unify to seconds
    duration_start="$startday "$(eval echo \$$duration|cut -d , -f 1)
    duration_end="$startday "$(eval echo \$$duration|cut -d , -f 2)
    #echo start:${duration_start}, end: ${duration_end}
    stdstart=$(date -d "${duration_start}" +%s)
    stdend=$(date -d "${duration_end}" +%s)

    cinemaName=$(arrayGet cinemas ${cinemaId})

 echo "city type:$prefix, cinema: $cinemaId, cinemaName: $cinemaName,hallId: $hallId, movieId:$movieId ,plan $planId, time is $starttime, weekday is $weekday, marketPrice is $marketPrice, movieType is $movieType"

: << BLOCKCOMMENT
  #special handling for foreign movies
    foreignPricetemp="foreignPrice_$prefix"
    foreignPrice=$(eval echo \$${foreignPricetemp})
    isForeign=0
    for((i=0; i<${#foreign_movies[*]}; i++))
        do
            echo foreignPrice is $foreignPrice, prefix is $prefix
            if [ "$movieId" -eq "${foreign_movies[i]}" ];then
                isForeign=1
                targetPrice="$foreignPrice"

                break

            fi

        done
BLOCKCOMMENT

    discount=$(eval echo \$${price_rule}|cut -d , -f 2)

    #special handling,
    if [ ${cinemaId} -eq 155 ] || [ ${cinemaId} -eq 153 ] || [ ${cinemaId} -eq 103 ] ||[ ${cinemaId} -eq 142 ] ;then
	    discount=0.7
	    #default_price=30

    fi

    primetime=1
    if [ ${startsec} -ge ${stdstart} ] && [ ${startsec} -le ${stdend} ];then

       targetPrice=$default_price
       primetime=0
       echo default case target is :$targetPrice, real is $price,primetime is $primetime
    else
        targetPrice=$(echo $marketPrice $discount | awk '{printf "%.1f", $1*$2 }')
        echo discount case: target is $targetPrice,real is  $price, primetime is $primetime
    fi

    result=$(echo $targetPrice $price|awk '{printf "%f", $1-$2}')
    result=$(echo $result-0|bc)

    if [ $result != 0 ];then
        #excel will filter numbers larger than 11 digits, so add single quote
        echo "$prefix,$cinemaId,$cinemaName,$hallId,$movieId,'$planId,$starttime,$weekday,$marketPrice,$price,$targetPrice,$movieType,,$primetime" >> "./wrongprice.csv"
    fi

}

#two arguments: cinemaId, file_prefix
processPlans(){
    cinemaId=$1
    prefix=$2


   enc=$(echo -n ${cinemaId}${planMethod}${timestamp}${uid}${passwd}|md5sum|cut -d ' ' -f 1)
   requrl="$SERVER?cinemaId=${cinemaId}&method=${planMethod}&time_stamp=${timestamp}&uid=${uid}&enc=${enc}"

   rawfile="raw/${prefix}_${cinemaId}.json"

   formatfile="format/${prefix}_${cinemaId}.format"
   curl  -s "${requrl}" -o ${rawfile}

    #cat temp|python -mjson.tool > ${rawfile}
    cat $rawfile|${dir}/JSON.sh -l > ${formatfile}

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
    movieType=$(grep "planInfo\",$index,\"movieType\"" ${formatfile}|cut -f 2|cut -d '"' -f 2)
    isIMAX=$(echo $movieType|grep -o 'IMAX\|DMAX')
    movieId=$(grep "planInfo\",$index,\"movieId\"" $formatfile|cut -f 2)

    #VIP,巨幕，贵宾厅，三个都是原价
    #VIP,vip
    #"\u8d35\u5bbe\u5385"
    #"\u5de8\u5e55\u5385"
    vipHall=$(grep "planInfo\",$index,\"hallName\"" ${formatfile}|grep -o "\\\u8d35\\\u5bbe\\\u5385\|vip\|VIP\|\\\u5de8\\\u5e55\\\u5385")
    cinemaName=$(arrayGet cinemas $cinemaId)
    arrayGet cinemas $cinemaId
    if [ -n "$isIMAX" ];then
        result=$(echo $marketPrice - $price|bc)
            echo "city type:$prefix, cinema: $cinemaId, cinemaName: $cinemaName, hallId: $hallId, movieId: $movieId, plan $planId, time is $starttime, weekday is $weekday, marketPrice is $marketPrice,movie type is $movieType"
        if [ $result -ne 0 ];then
            echo "$prefix,$cinemaId,$cinemaName,$hallId,$movieId,'$planId,$starttime,$weekday,$marketPrice,$price,$targetPrice","$movieType" >> "./wrongprice.csv"
        fi
    elif [ -n "$vipHall" ];then
        result=$(echo $marketPrice - $price|bc)
            echo "city type:$prefix, cinema: $cinemaId, cinemaName: $cinemaName,hallId: $hallId, movieId: $movieId,plan $planId, time is $starttime, weekday is $weekday, marketPrice is $marketPrice, viphall is $(printf $(eval echo "$vipHall"))"
        if [ $result -ne 0 ];then
            echo "$prefix,$cinemaId,$cinemaName,$hallId,$movieId,'$planId,$starttime,$weekday,$marketPrice,$price,$targetPrice","$movieType",$(printf $(eval echo "$vipHall"))>> "./wrongprice.csv"
        fi
    else

        #NOTE: double quote is IMPORTANT when argument including space!!!
        processPrice $cinemaId $prefix "$timeString" $marketPrice $price $planId $hallId $movieId $movieType
    fi




done

}



#use this line to do unit test, handle one movie
# processPrice $1 $2 "$3" $4 $5 $6 $7 $8
#handle one cinema
#processPlans 103 "first"
#processPlans 104 "second"
#shell blockcomment
: << BLOCKCOMMENT
BLOCKCOMMENT




genCinemaPair


#declare the global variable
while read line
do
    cid=$(echo $line|cut -d, -f 1)
    cname=$(echo $line|cut -d, -f 2)
    declare "cinemas_$cid=$cname"
done < cinema.pair

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

: << BLOCKCOMMENT


#special cities
for((i=0; i<${#SPECIALCITIES[*]}; i++))
#for((i=0; i<1; i++))
do
    cinemaId=${SPECIALCITIES[i]}
    processPlans $cinemaId "special"
done
BLOCKCOMMENT


rm -f temp
