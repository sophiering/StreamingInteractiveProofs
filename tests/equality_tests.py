# equality tests
import unittest
from protocols.equality import equality_check

class TestClass(unittest.TestCase):
    # ensure 
    def test_same(self):
        input1 = [1,2,3,4] # input()
        input2 = [1,2,3,4] # input() 
        input = input1 + input2
        self.assertTrue(equality_check(input))
    def test_permuation(self):
        input1 = [1,2,3,4] # input()
        input2 = [2,4,3,1] # input() 
        input = input1 + input2
        self.assertFalse(equality_check(input))
    def test_different(self):
        input1 = [1,2,3,4] # input()
        input2 = [2,4,5,1] # input() 
        input = input1 + input2
        self.assertFalse(equality_check(input))

