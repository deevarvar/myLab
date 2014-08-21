__author__ = 'deevarvar'
import random
import unittest
import sys
import os
from subprocess import call
print os.getcwd()
current_path = os.path.dirname(os.path.realpath(__file__))

lib_path = current_path + "/../../utlib"
make_path = current_path + "/../../"
print 'lib path is ' + lib_path + ', make path is ' + make_path
sys.path.append(lib_path)
import ut_util
from subprocess import call



#TODO:
#1. add function to process random string
#2. compare two files' content

class TestCopyFile(unittest.TestCase):
    def setUp(self):
        print 'setup steps:'
        print 'change dir'
        call(['cd', make_path])
        print 'compile binary to make file '
        call(['make'])


    #TODO: test file name limits http://serverfault.com/questions/9546/filename-length-limits-on-linux

    #test file content
    #empty file
    def test_empty_file(self):
        print 'generate src and dst files:'
        src_file_name = "src_" + ut_util.string_generator(8)
        dst_file_name = "dst_" + ut_util.string_generator(8)
        ut_util.touchFile(src_file_name)
        ut_util.touchFile(dst_file_name)
        print 'src file is '+ src_file_name + ", dst_file_name is " + dst_file_name

        src_content = ut_util.string_generator(1025)
        with open(src_file_name, 'w') as src:
            src.write(src_content)

        call(['cd', make_path + '/ut/'])
        call(['./copy', src_file_name, dst_file_name])

        print 'do the compare of file content'
        with open(src_file_name, 'r') as src:
            with open(dst_file_name, 'r') as dst:
                self.assertEqual(src.read(), dst.read())

#100 chars

#1024 chars


    #more than 1024 chars, 2000 chars


if __name__ == '__main__':
    unittest.main()