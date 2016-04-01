#!/bin/bash

declare -a libdir=("avatar" "adapter" "lemon" "melon" "watermelon" "grape" "service" "security" "app" "ImsCm")

: > committeremail.tmp
for lib in "${libdir[@]}"
do
        echo start to check "$lib" 
	cd $lib
	git log --pretty=format:"%ce" >> ../committeremail.tmp
	echo >> ../committeremail.tmp
	cd ..
done

cat committeremail.tmp | sort | uniq > committeremail


#git log --pretty=format:"%h;%ce" |grep -Ev ".*@juphoon.com.*|.*gerrit.*"
