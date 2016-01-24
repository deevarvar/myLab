# -*- encoding=utf-8 -*-
# @description: add ike and esp keys to wireshark settings
# @author: zhihuaye<zhihua.ye@spreadtrum.com>


import os
import re
import easygui
import glob


def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
    print ''.join(map(either,pattern))
    return glob.glob(''.join(map(either,pattern)))

print insensitive_glob('./*.log')






