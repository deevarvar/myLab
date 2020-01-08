# -*- coding:utf-8 -*-
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
import unittest
from List import ListNode, List 

class PalTest(unittest.TestCase):
    TEST_DATA = [
            ([], True),
            ([10,2,3], False),
            ([56,100,100,56], True),
            ([1,2,3,2,1], True)
            ]
    def setUp(self):
        self.judge = Palindrome()

    def test_rev(self):
        for nodes, exp in self.TEST_DATA:
            newl = List()
            for node in nodes:
                newl.append(node)
            rh = self.judge.reverse(newl.head)
            print List(head=rh)

    def test_pal(self):
        for nodes, exp in self.TEST_DATA:
            newl = List()
            for node in nodes:
                newl.append(node)
            print "listinfo is {}".format(newl)
            self.assertEqual(self.judge.isPalindrome(newl.head), exp)

class Palindrome:
    def isPalindrome(self, pHead):
        # just reverse latter ones
        if pHead == None:
            return True
        fast = pHead
        slow = pHead
        while slow:
            fast = fast.next
            if fast:
                fast = fast.next
                if fast:
                    slow = slow.next
                else: 
                    break
            else:
                break
        mid = slow
        print "mid is {}".format(mid)
        # reverse latter half
        rev = self.reverse(mid.next)        
        print "reverse part is {}".format(List(head=rev))
        # compare from start
        start = pHead
        while rev:
            if start.val == rev.val:
                start = start.next
                rev = rev.next
            else:
                return False 
        return True

    def reverse(self, pHead):
        print "rev head is {}".format(pHead)
        curr = pHead
        prev = None
        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        return prev

    def isPalindromeUsingStack(self, pHead):
        # use stack to record first half
        pass

if __name__ == '__main__':
    unittest.main()
