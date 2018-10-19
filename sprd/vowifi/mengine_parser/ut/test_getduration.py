# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com

import unittest
import os
import sys
sys.path.append('../')
from lib.logutils import *


class TestGetDuration(unittest.TestCase):
    def setUp(self):
        self.logutils = logutils()

    def tearDown(self):
        pass

    def test_one(self):
        fruitbegin = "08-31 16:18:20.260"
        fruitend = "08-31 16:18:21.260"
        begin = self.logutils.converttime(fruitbegin)
        end = self.logutils.converttime(fruitend)
        duration = end - begin
        print duration

if __name__ == "__main__":
    unittest.main()