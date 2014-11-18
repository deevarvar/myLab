__author__ = 'deevarvar'
"""
the same function as process.sh do

"""

with open('log_temp.txt', 'r') as log_file:
    for line in log_file:
        print("-------"+line)
        index = line.find(' ')
        print("part one is "+line[:index])
        #trip leading spaces
        trim_remain = line[index:].lstrip()
        #print(trim_remain);
        flag = trim_remain.find(' ')
        if flag == -1:
            print("part two is empty!")
            print("part three is " + trim_remain)
        else:
            print("part two is " + trim_remain[0:flag])
            last_remain = trim_remain[flag:].lstrip()
            print("part three is "+last_remain)
