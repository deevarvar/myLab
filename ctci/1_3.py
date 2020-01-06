import unittest

class SameTest(unittest.TestCase):
    TEST_DATA = [
            ("abc", "cba", True),
            ("aaaa", "bbb",False),
            ("abc", "cbacba", False)
            ]
    def setUp(self):
        self.judge = Same()

    def test_same(self):
        for strA, strB, expect in self.TEST_DATA:
            self.assertEqual(self.judge.checkSam(strA,strB), expect)

class Same:
    def checkSam(self, stringA, stringB):
        # write code here
        amap = {}
        for letter in stringA:
            amap.setdefault(letter, 0)
            if letter in amap:
                amap[letter] += 1

        for letter in stringB:
            if letter not in amap:
                return False
            if letter in amap:
                if amap[letter] > 0:
                    amap[letter] -=1
                else:
                    return False
        return all(amap.values()) is False


if __name__ == "__main__":
    unittest.main()
