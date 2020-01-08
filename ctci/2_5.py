# -*- coding:utf-8 -*-

import unittest
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Plus:
    def plusAB(self, a, b):
        # write code here
        carr = 0
        acurr = a
        bcurr = b
        ret = ListNode(0)
        head = ret
        while acurr and bcurr:
            tmp = acurr.val + bcurr.val + carr
            carr = tmp/10
            new = ListNode(tmp%10)
            head.next = new
            head = new
            acurr = acurr.next
            bcurr = bcurr.next

        if acurr is None and bcurr is None and carr != 0:
            new = ListNode(carr)
            head.next = new

        while acurr:
            new = ListNode(acurr.val + carr)
            carr = 0
            head.next = new
            head = new
            acurr = acurr.next

        while bcurr:
            new = ListNode(bcurr.val + carr)
            carr = 0
            head.next = new
            head = new
            bcurr = bcurr.next

        return ret.next
