__author__ = 'deevarvar'
import random
import unittest
import sys
import os
print os.getcwd()

current_path = os.path.dirname(os.path.realpath(__file__))
print current_path
lib_path = current_path + "/../../utlib"
sys.path.append(lib_path)
from gen_string import util

#TODO:
#1. add function to process random string
#2. compare two files' content

class TestCopyFile(unittest.TestCase):
    def setUp(self):
        print 'setup steps:'
        print '1. compile binary'
        print '2. create source file'
        print string_generator(8)

    def test_long_file_name(self):
        #test long file name
        print 'in one case'




if __name__ == '__main__':
    unittest.main()