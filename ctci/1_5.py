# -*- coding:utf-8 -*-

import unittest

class TestZip(unittest.TestCase):
    TESTDATA = [
            ("aabbb" , "a2b3"),
            ("aaaa", "a4"),
            ("abc", "abc"),
            ("abcdd","abcdd")
            ]
    def setUp(self):
        self.judge = Zipper()

    def testsame(self):
        for src, exp in self.TESTDATA:
            self.assertEqual(self.judge.zipString(src),exp)

class Zipper:
    def zipString(self, iniString):
        # write code here
        record = []
        prevchar = None
        prevlen = 0

        for letter in iniString:
            if letter == prevchar:
                prevlen += 1
            else:
                if prevlen > 0:
                    record.append({prevchar : prevlen})
                prevlen = 1
                prevchar = letter
        if prevlen > 0:
            record.append({prevchar : prevlen})
        newstring = ''
        for item in record:
            for key,value in item.iteritems():
                newstring += "{}{}".format(key,value)
        return newstring if len(newstring) < len(iniString) else iniString

            
if __name__ == '__main__':
    unittest.main()
