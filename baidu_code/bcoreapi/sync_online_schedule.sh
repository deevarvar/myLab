table_name=$1
rm schedule.sql
#/home/work/.jumbo/bin/mysqldump -h yf-dba-map-user-99.yf01 -P 3306 -umiliang -pW6G02SVh5Z --skip-lock-tables instant_info $1  > schedule.sql
/home/work/.jumbo/bin/mysqldump -h 10.81.10.49 -P 5108 -umiliang -pW6G02SVh5Z --skip-lock-tables instant_info $1  > schedule.sql
/home/work/.jumbo/bin/mysql instant_info_dq < schedule.sql -h 10.94.34.24 -P 3306 -uroot -proot
