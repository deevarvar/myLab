class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.num = capacity
        self.l = []
        self.keys = {}        

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if self.keys.has_key(key):
            self.l.remove(key)
            self.l.insert(0,key)
            return self.keys[key]
        else:
            return -1        

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if self.keys.has_key(key):
            self.l.remove(key)
        elif len(self.l) == self.num:
            trash = self.l.pop()
            self.keys.pop(trash)

        self.keys[key] = value
        self.l.insert(0, key)

cache = LRUCache(2) 
cache.put(1, 1)
cache.put(2, 2)
print cache.get(1)       # returns 1
cache.put(3, 3)    # evicts key 2
print cache.get(2)       # returns -1 (not found)
cache.put(4, 4)    # evicts key 1
print cache.get(1)       # returns -1 (not found)
print cache.get(3)       # returns 3
print cache.get(4)       # returns 4
