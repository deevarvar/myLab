#!/bin/bash

declare -a libdir=("avatar" "adapter" "lemon" "melon" "watermelon" "grape" "service" "security" "app" "strongswan")
postfix=$(date +%Y%m%d)

rn=$(pwd)/release_$postfix.note
: > $rn
rntmp=$rn.tmp
echo $rntmp
for dir in "${libdir[@]}"
do
	echo in $dir
	cd $dir
#	commitid=$(git rev-parse --short HEAD)
#	logformat=$(git log --pretty=format:"%h%x09%an%x09%ad%x09" -1)
	logformat=$(git log -1 --pretty=format:'%h|%ad|%an')
	echo $logformat
	echo "$dir $logformat" >> $rntmp
	cd ..
done

cat $rntmp | column -ts '|' > $rn
