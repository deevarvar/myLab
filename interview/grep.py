#http://stackoverflow.com/questions/9000960/python-regular-expressions-re-search-vs-re-findall?rq=1
#https://docs.python.org/2/howto/regex.html
#use non-capture version in findall

import re


def find_ip(file_name):
    with open(file_name, 'r') as ip_file:
        for line in ip_file:
            #print(line),
            #digit_pattern = '[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-6]'
            ip_pattern = '(?P<ip>\\b(?P<sub>(?P<digit>[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-6])\.){3}' \
                         '(?P<last>[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-6])\\b)'

            m = re.search(ip_pattern, line)
            if m is not None:
                #print(m.groups())
                print(m.group('ip'))

find_ip('./source_file/ip.txt')


def find_mac(file_name):
    with open(file_name, 'r') as mac_file:
        for line in mac_file:
            mac_pattern = line
