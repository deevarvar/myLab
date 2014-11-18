__author__ = 'deevarvar'


"""
some idea from baidu's interview

1. this file is used to generate the some file template
three column
column1    column2                  column3
chars      chars(or empty)          digits


try to use shell or python to finish
"""
import random
import string

def gen_seperator():
    var_len = random.randint(1, 10)
    space = ' '
    for index in range(var_len):
        space += ' '
    return space


def gen_column_one():
    var_len = random.randint(1, 10)
    return ''.join(random.choice(string.ascii_letters) for _ in range(var_len))


def gen_column_two():
    choice = random.randint(0,100)
    if choice >= 50:
        return ' '
    else:
        var_len = random.randint(1, 10)
        return ''.join(random.choice(string.ascii_letters) for _ in range(var_len))


def gen_column_three():
    var_len = random.randint(1, 10)
    return ''.join(random.choice(string.digits) for _ in range(var_len))


with open('./baidu_interview/log_temp.txt', 'w') as log:
    for i in xrange(0, 10):
        log.write(gen_column_one()+gen_seperator()+gen_column_two()+gen_seperator()+gen_column_three()+'\n')