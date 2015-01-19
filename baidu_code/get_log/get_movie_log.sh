#!/bin/bash

#author: yezhihua@baidu.com
#desc:   从hadoop集群抓取moive的log

#hadoop-client manual: http://wiki.baidu.com/pages/viewpage.action?pageId=41884764#Hadoop-v2FsshellIntroduction-dus
# TODO: 1.root cause of missing log


#warning file: /log/40344/odp_movie_lsp/20150104/0100/nj02-orp-app1049.nj02.baidu.com/ticket.log.wf.2015010401.63
#trace file: /log/40344/odp_movie_trace_lsp/20150104/0000/hz01-orp-app0144.hz01.baidu.com/ticket.log.2015010400.23

#console foreground color
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
white=`tput setaf 7`
blue=`tput setaf 4`
reset=`tput sgr0`
bold=`tput bold`
#variable definition
NO_ARG=0
DAY_LEN=8
HOUR_LEN=10
HADOOP=hadoop-client/hadoop/bin/hadoop
HADOOP_LS="$HADOOP fs -ls"
HADOOP_LSR="$HADOOP fs -lsr"
HADOOP_GET="$HADOOP fs -get"

#default value
#似乎没有好的办法知道当前机器总数，大概是80
#认为如日志如果少于90%，那么有异常
LOG_NUM=79
PASS_RATE=0.9

#逻辑是， 第一次用-get获取目录
#如果失败，那么那么用-get获取单个file
RETRY_TIMES=3 #only retry 2 times
WATER_LINE=$(echo $LOG_NUM*$PASS_RATE|bc)
WATER_LINE=${WATER_LINE%.*}

#retry rules
#crontab job is start at 20mins
#if 1st retry thresthhold is 50%, +5mins sleep
#if 2nd retry threshhold is 75%, +5mins sleep
baseSleep=300
threshholdArray=(0 0.5 0.75)
deltaSleep=(0 300 300)

MODULE=${2:-ticket}
LOG_LEVEL=${3:-warning}



TRACE_DIR=/log/40344/odp_movie_trace_lsp
WARN_DIR=/log/40344/odp_movie_lsp
TARGET_DIR=""
WARN_FILE="ticket.log.wf.*"
TRACE_FILE="ticket.log.*"


usage(){
    print_notice "`basename $0` should be used with hadoop-client"
    print_notice "Usage: sh ${yellow}`basename $0` date module log_level.${reset}"
    print_notice "date is the log date, default is the latest"
    print_notice "module name can be ${yellow}${bold}ticket/info${reset}, default is ${bold}${yellow}ticket.${reset}"
    print_notice "log_level can be ${yellow}${bold}trace/warning${reset}, default is ${bold}${yellow}warning${reset}."

}


print_log(){
    timestamp=`date +%Y%m%d%H%M%S`
    echo "$timestamp [LOG]"$1
}


print_notice(){
    timestamp=`date +%Y%m%d%H%M%S`
    echo "$timestamp ${yellow}[NOTICE]${reset}$1"
}


print_error(){
    timestamp=`date +%Y%m%d%H%M%S`
    echo "$timestamp ${red}[ERROR]$1${reset}"
}


notify_admin(){
    timestamp=`date +%Y%m%d%H%M%S`
    cat $1 | mail -s "failed to get log at $timestamp" yezhihua@baidu.com
}


get_orp_log(){

    #argument check
    if [ $# -ne 3 ];then
        print_error "get_orp_log need 3 arguments: date, module, log_level"
        exit -1
    fi
    start_time=$(date +%Y%m%d%H%M%S)
    print_log "Start:${start_time},date:$1,module:$2,log_level:$3"

    #check hadoop client
    if [ ! -f $HADOOP ]; then
        print_error "$HADOOP not found!"
        exit -1
    fi

    #construct the dir
    if [ $3 == "warning" ];then
        TARGET_DIR=$WARN_DIR
    else
        TARGET_DIR=$TRACE_DIR
    fi

    #get date
    DATE_DIR=${1:0:8}
    HOUR_DIR=${1:8:2}
    print_log "date dir is $DATE_DIR, hour dir is $HOUR_DIR"
    if [ -z  $HOUR_DIR ];then
        TARGET_DIR="$TARGET_DIR/$DATE_DIR/"
	    print_notice "you choose a whole day's log."
	    #whole log download do not retry...
	    RETRY_TIMES=1
    else
        TARGET_DIR="$TARGET_DIR/$DATE_DIR/"$HOUR_DIR"00/"
    fi

    #check if dir exist
    $HADOOP_LS $TARGET_DIR > /dev/null

    if [ $? -eq 0 ];then
        #retry at most $RETRY_TIMES times
        count=0
        while ((count < RETRY_TIMES)); do

            temp_dir=$3_$1_${start_time}_$count

            ((count++))
           	print_notice "[$count]start to download ${yellow}$3 log${reset} to logs/$temp_dir, may take some time..."
	        mkdir -p logs/$temp_dir/original
	        mkdir -p logs/$temp_dir/archive

            start=$(date +%s)
            #record log
                if [ $3 == "warning" ];then
                    target_file=$WARN_FILE
                else
                    target_file=$TRACE_FILE
                fi

            if [ $count -eq 1 ]; then
                $HADOOP_GET $TARGET_DIR logs/$temp_dir/original/ >logs/$temp_dir/email_content 2>&1
                cp -a $(find logs/$temp_dir/original -name "$target_file") logs/$temp_dir/archive/
            else
                #get file list
                $HADOOP_LSR $TARGET_DIR 2>logs/$temp_dir/email_content | grep "$target_file" | awk '{print $8}' > logs/$temp_dir/files_list
                    while read line
                        do
                            $HADOOP_GET $line logs/$temp_dir/archive/
                        done < logs/$temp_dir/files_list

            fi
            #record exit status

            end=$(date +%s)
            echo "duration:$(($end-$start))s" | tee -a logs/$temp_dir/download_info
            files_num=$(find logs/$temp_dir/archive/ -name "$target_file" -type f|wc -l)
            echo "files_num:$files_num" | tee -a logs/$temp_dir/download_info
            echo "files_size:$(du -sh logs/$temp_dir/archive/|awk '{print $1}')"|tee -a logs/$temp_dir/download_info
	        #add email content in case
    	    cat logs/$temp_dir/email_content
            cat logs/$temp_dir/download_info >> logs/$temp_dir/email_content
            print_notice "you can find your log in ${yellow}logs/$temp_dir/archive/${reset}"


            #check if the file number is correct
            #TODO: need to check file's checksum
	        if [ $files_num -ge $WATER_LINE ];then
    	        break
        	else
        	    deltaTime=0
        	    downloadRate=$(echo "$files_num/$LOG_NUM"|bc -l)
        	    pass=$(echo "$downloadRate < ${threshholdArray[$count]}"|bc -l)

        	    if [ $pass -ne 0 ];then
        	        deltaTime=${deltaSleep[$count]}
        	    fi

        		wait_time=$(echo "$baseSleep*$count+$deltaTime"|bc)
        		print_error "date:$1,module:$2,log_level:$3" | tee -a logs/$temp_dir/email_content
            	print_error "only download $files_num/$LOG_NUM in $(readlink -f logs/$temp_dir/archive), will retry in $wait_time seconds" | tee -a logs/$temp_dir/email_content
        		notify_admin logs/$temp_dir/email_content
				sleep $wait_time 
			fi

        done

        if [ $count -ne 1 ];then

            if [ $count -ge $RETRY_TIMES ]; then

                print_error "retry $RETRY_TIMES times, log still failed to get $target_hour"
            else
                print_notice "after retry $count times, log can be fetched."
            fi

        fi

    else
        print_error "$TARGET_DIR does not exist!"
    fi

    end_time=$(date +%Y%m%d%H%M%S)
    print_log "End:${end_time},date:$1,module:$2,log_level:$3"
}


mkdir -p logs
target_hour=`date --date='1 hours ago' "+%Y%m%d%H"`
target_day=`date "+%Y%m%d"`

if [ $# -eq $NO_ARG ];then
    print_notice "no arguments is specified and get the latest trace/warning log."
    print_notice "date:  ${yellow}$target_hour${reset}" 
    #print_notice "module: ${yellow}$MODULE${reset}"
    #print_notice "log_level: ${yellow}$LOG_LEVEL${reset}"
    get_orp_log $target_hour ticket warning
    get_orp_log $target_hour ticket trace
else
    #first argument MUST be date: length and value check
    #module ,log_level is optional.
    if [ ${#1} -eq $DAY_LEN -a $1 -le $target_day ] || [ ${#1} -eq $HOUR_LEN -a $1 -le $target_hour ];then
	print_notice "date:  ${yellow}$1${reset}" 
    	print_notice "module: ${yellow}$MODULE${reset}"
    	print_notice "log_level: ${yellow}$LOG_LEVEL${reset}"
    	get_orp_log $1 $MODULE $LOG_LEVEL
    else
        print_error "invalid date! Only log before $target_day/$target_hour can be fetched."
        usage
    fi

fi

