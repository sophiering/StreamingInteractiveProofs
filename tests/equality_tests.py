# equality tests
import unittest
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from stream_generation.gen_equality import gen_test
from protocols.equality import equality_check, equality_t, equality_f

class TestClass(unittest.TestCase):
    # ensure 
    def test_same(self):
        input1 = [1,2,3,4] # input()
        input2 = [1,2,3,4] # input() 
        input = gen_test("equal.txt", input1, input2)
        answer, _ = equality_check(input)
        self.assertTrue(answer)
    def test_permuation(self):
        input1 = [1,2,3,4] # input()
        input2 = [2,4,3,1] # input() 
        input = gen_test("equal.txt", input1, input2)
        answer, _ = equality_check(input)
        self.assertFalse(answer)
    def test_different(self):
        input1 = [1,2,3,4] # input()
        input2 = [2,4,5,1] # input() 
        input = gen_test("equal.txt", input1, input2)
        answer, _ = equality_check(input)
        self.assertFalse(answer)
    def test_t(self):
        answer, _ = equality_t("equality.txt")
        self.assertTrue(answer)
    def test_f(self):
        answer, _ = equality_f("equality.txt")
        self.assertFalse(answer)

