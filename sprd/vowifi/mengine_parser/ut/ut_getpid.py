#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com


import unittest
import os
import sys
sys.path.append('../')
import definition
from mflow_parser import mflow

#define a struct to collect all the cases

class case():
    def __init__(self,description, lines, result):
        self.desc = description
        self.lines = lines
        self.result = result

    def getdesc(self):
        return self.desc

    def getlines(self):
        return self.lines

    def getresult(self):
        return self.result


class TestGetPid(unittest.TestCase):
    def setUp(self):
        count = 0
        self.cases = list()

        #case1
        des = "androidO line, one match"
        lines = list()
        lines.append("02D429 08-31 16:18:20.260  4117  4286 I MME     : 16:18:20.260 MVD: INFO: StrmOpen rtp timeout 5 ")
        result = dict()
        result['num'] = 1
        #pid is list
        result['pid'] = ['4117']
        caseone = case(description=des, lines=lines, result=result)
        self.cases.append(caseone)

        logname = str(count) + ".log"
        with open(logname, 'w') as log:
            for index, line in enumerate(lines):
                log.write(line)
        #case2
        des = "non-androidO line, two match"

        #case3
        des = "messy code exist in pid field"

    def test_one(self):
        count = 0
        for index, case in enumerate(self.cases):
            logname = str(count) + '.log'
            mins = mflow(logname=logname)
            mins.findPid()
            result = case.getresult()
            self.assertEqual(result['num'], len(mins.pid))
            self.assertListEqual(result['pid'], mins.pid)
            count = count + 1

    def tearDown(self):
        for count in range(0, len(self.cases)):
            try:
                filename = str(count) + '.log'
                os.remove(filename)
            except OSError:
                pass

if __name__ == "__main__":
    unittest.main()
