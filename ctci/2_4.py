# -*- coding:utf-8 -*-
import unittest
import random

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def append_list(head, val):
    if head:
        newnode = ListNode(val)
        head.next = newnode

def iter_node(head):
    while head:
        print "-->{}".format(head.val)
        head = head->next

class PartTest(unittest.TestCase):
    head1 = ListNode(1)
    append_list(head1, 2)
    append_list(head1, 3)
    append_list(head1, 4)
    exphead = head1
    def setUp(self):
        pass

    def test_part(self):
        # construct new list
        pass

class Partition:
    def partition(self, pHead, x):
        # write code here
        pass

if __name__ == '__main__':
    unittest.main()
