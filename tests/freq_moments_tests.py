# frequency moments tests
import unittest
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from stream_generation.gen_freq_moments import f_1_s,f_2_s
from protocols.freq_moments import f_1, f_2_t, f_2_f


class TestClass(unittest.TestCase):
    # 1st frequency moment
    def test_f_1(self):
        n = f_1_s("f_1_test.txt")
        self.assertEqual(f_1("f_1_test.txt"), n)
    # 2nd frequency moment
    def test_true(self):
        f_2_s("f_2_test.txt")
        # TODO : figure out what this should be
        # self.assertEqual(f_2_t("f_2_test.txt"), )
    def test_bad_h(self):
        f_2_s("f_2_test.txt")
        self.assertEqual(f_2_f("f_2_test.txt"), -1)


