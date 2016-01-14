#!/bin/bash

#### params
INFO_CASE_PATH='/home/map/miliang/new_api_auto_test/info'
TICKET_CASE_PATH='/home/map/miliang/new_api_auto_test/ticket'
INFO_CASE_LIST=("cinema_index.py" "cinema_detail.py" "cinema_comment.py" "schedule.py" "movie_index.py" "movie_detail.py" "movie_comment.py" "cinema_sfrom_rule.py")
TICKET_CASE_LIST=("old_seat_info.py" "seat_info.py" "lock_seat.py" "order_query.py" "old_lock_seat.py")


#### execute
cd /home/map/miliang/new_api_auto_test

# update info
echo "::::Auto Test::::Start to update sql info..."
#sh sync_online_schedule.sh t_movie_guid
#sh sync_online_schedule.sh t_movie_poi
#sh sync_online_schedule.sh t_movie_info
#sh sync_online_schedule.sh t_movie_cinemas
#sh sync_online_schedule.sh t_movie_sms_cinema
#sh sync_online_schedule.sh t_movie_sms_template
#sh sync_online_schedule.sh t_movie_machine
#sh sync_online_schedule.sh t_movie_theater
#sh sync_online_schedule.sh t_movie_third_theater
#sh sync_online_schedule.sh t_movie_cache_odp

#sh sync_online_schedule.sh t_movie_cinemas_fee
#sh sync_online_schedule.sh t_movie_pact
#sh sync_online_schedule.sh t_movie_pact_cinemas
#sh sync_online_schedule.sh t_movie_price_rule
#sh sync_online_schedule.sh t_movie_price_rule_movie_type
#sh sync_online_schedule.sh t_movie_price_rule_theater
#sh sync_online_schedule.sh t_movie_sms_cinema


# execute case
echo "::::Auto Test::::Start to execute cases..."

# info cases
cd $INFO_CASE_PATH
for case in ${INFO_CASE_LIST[@]}
    do
        trap "echo Case $case Failed!!!;exit" ERR
	echo "::::Auto Test::::Case: $case starts."
	/home/map/.jumbo/bin/python $case
    done

# ticket cases
cd $TICKET_CASE_PATH
for case in ${TICKET_CASE_LIST[@]}
    do
	trap "echo Case $case Failed!!!;exit" ERR 
	echo "::::Auto Test::::Case: $case starts."
	/home/map/.jumbo/bin/python $case
    done
