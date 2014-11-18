__author__ = 'deevarvar'

import random

with open('./array.h', 'w') as header_file:
    header_file.write("int array[] = {\n")
    for index in xrange(0,10):
        header_file.write(str(random.randint(0,100)) + ",\n")
    header_file.write("};")