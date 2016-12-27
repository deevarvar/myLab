#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
#some event helper for searchEvent in flowParser.py
import re

def matchone(match):
    '''
    return the first match one
    :param match:
    :return:
    '''
    grouplen = len(match.groups())
    if match and grouplen >= 1:
        return match.group(1)
    else:
        return None



if __name__ == '__main__':
    key = 'abc'
    line = "abc"
    pattern = re.compile(key)
    match = pattern.search(line)
    print matchone(match)