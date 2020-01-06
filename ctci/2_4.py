# -*- coding:utf-8 -*-
import unittest
from List import ListNode, List 
class PartTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_part(self):
        # construct new list
        pass

class Partition:
    def partition(self, pHead, x):
        # write code here
        slist = List()
        blist = List()
        newlist = List()
        exist = False
        while pHead:
            if pHead.val < x:
                slist.append(pHead.val)
            elif pHead.val >= x:
                blist.append(pHead.val)
            pHead = pHead.next
        print "bigger is {}".format(blist)
        print "smaller is {}".format(slist)
        scurr = slist.head
        bcurr = blist.head
        while scurr:
            newlist.append(scurr.val)
            scurr = scurr.next
        while bcurr:
            newlist.append(bcurr.val)
            bcurr = bcurr.next
        print newlist
        return newlist.head

if __name__ == '__main__':
    l = List()
    l.append(5)
    l.append(1)
    l.append(4)
    l.append(3)
    l.append(2)
    print l 
    judge = Partition()
    print judge.partition(l.head, 4)
    l = List()
    l.append(3)
    l.append(3)
    l.append(3)
    print l
    print judge.partition(l.head, 3)     
