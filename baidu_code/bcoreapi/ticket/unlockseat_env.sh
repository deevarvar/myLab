#!/bin/bash

dbnames=(t_movie_cache_odp t_movie_poi t_movie_third_theater) 


onlinedb=10.81.10.49
onlineport=5108

pool1db=10.94.34.26
pool1port=3305

function updateNeeded(){
for((i=0;i<${#dbnames[*]};i++))
do
        table=${dbnames[i]}
        updatedb $table
done
}
function updatedb(){
        echo backup $1, enter password for $onlinedb,username is yezhihua
        mysqldump -u yezhihua -h $onlinedb -P $onlineport --skip-lock-tables --default-character-set=utf8 -pbaidu123 instant_info $1> $1.sql
        echo restore $1, enter password for localdb, username is root
        mysql --max_allowed_packet=100M -u root -proot -h $pool1db -P $pool1port instant_info --default-character-set=utf8  -proot< $1.sql


}


updateNeeded
