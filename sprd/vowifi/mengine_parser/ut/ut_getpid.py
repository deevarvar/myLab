#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com


import unittest
import os
import sys
sys.path.append('../')
from mflow_parser import mflow

#define a struct to collect all the cases

class onecase():
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
        caseone = onecase(description=des, lines=lines, result=result)
        self.cases.append(caseone)

        #case2
        des = "non-androidO line, two match"
        lines = list()
        lines.append("08-31 16:18:20.260  8000  4286 I MME     : 16:18:20.260 MVD: INFO: StrmOpen rtp timeout 5\n")
        lines.append("08-31 16:18:20.260  4000  4286 I MME     : 16:18:20.260 MVD: INFO: StrmOpen rtp timeout 5 ")
        result = dict()
        result['num'] = 2
        #pid is list
        result['pid'] = ['8000', '4000']
        casetwo = onecase(description=des, lines=lines, result=result)
        self.cases.append(casetwo)

        #case3
        des = "messy code exist in pid field"
        lines = list()
        lines.append("02D429 08-31 16:18:20.260  乱码  4286 I MME     : 16:18:20.260 MVD: INFO: StrmOpen rtp timeout 5 ")
        result = dict()
        result['num'] = 1
        #pid is list
        result['pid'] = [None]
        casethree = onecase(description=des, lines=lines, result=result)
        self.cases.append(casethree)

        for index, case in enumerate(self.cases):
            logname = str(count) + ".log"
            lines = case.getlines()
            with open(logname, 'w') as log:
                for index, line in enumerate(lines):
                    log.write(line)
            count = count + 1


    def test_AllInOne(self):
        count = 0
        for index, case in enumerate(self.cases):
            logname = str(count) + '.log'
            print case.getdesc()
            mins = mflow(logname=logname)
            mins.findPid()
            result = case.getresult()
            self.assertEqual(result['num'], len(mins.pids))
            self.assertListEqual(result['pid'], mins.pids)
            count = count + 1

    def tearDown(self):
        #clean up temp files
        for count in range(0, len(self.cases)):
            try:
                filename = str(count) + '.log'
                os.remove(filename)
            except OSError:
                pass

if __name__ == "__main__":
    unittest.main()
