# -*- coding:utf-8 -*-
import unittest
import random
import copy

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
    
    def __repr__(self):
        return repr(self.val)

class List:
    def __init__(self):
        self.head = None

    def append(self, data):
        if self.head is None:
            self.head = ListNode(data)            
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = ListNode(data)

    def remove(self, data):
        if self.head is None:
            return False
        curr = self.head
        prev = None
        while curr:
            if curr.val == data:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True
            else:
                prev = curr
                curr = curr.next
        return False

    def __repr__(self):
        disp = ''        
        curr = self.head
        while curr:
            disp += repr(curr) + "->"
            curr = curr.next 
        return disp + 'NULL'        

    def reverse(self):
        curr = self.head
        prev = None
        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        self.head = prev

    def __eq__(self, other):
        node = self
        if not self and not other:
            return True
        while node:
            if not other:
                return False
            if node.val == other.val:
                node = node.next
                other = other.next
            else:
                return False
        return False if other else True

if __name__ == '__main__':
    l = List()
    l.append(1)
    l.append(2)
    l.append(3)
    l.append(4)
    print l
    l.reverse()
    print l
