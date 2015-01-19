#!/bin/sh
#use to grep ip/email address
#find ip 100.100.100.100
grep -oE '((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])' source_file/ip.txt 
#grep -oE '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' source_file/ip.txt

#find mac : 11:22:33:44:55:66
grep -oE '\b[0-9a-zA-Z]{2}(:[0-9a-zA-Z]{2}){5}\b' source_file/ip.txt


#find email: zhiye@cisco.com
grep -oE '\b[0-9a-zA-Z._#%-]+@[A-Z0-9a-z.-]+\.[a-zA-Z]{2,4}\b' source_file/ip.txt
