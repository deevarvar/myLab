__author__ = 'deevarvar'

import string
import random
import os


#generate a random string
def string_generator(size=6, chars=string.ascii_letters+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#emulate touch cmd
def touchFile(fname, time=None):
    with open(fname, 'a'):
        os.utime(fname,time)
