# frequency moments tests
import unittest
import sys
import numpy as np
import galois as g
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from stream_generation.gen_freq_moments import f_s, f_1_test, f_2_s
from protocols.freq_moments import f_0_v, f_1_v, sketch_2d, h_2d_t, h_2d_f, verify

class TestClass(unittest.TestCase):
    # 0th frequency moment
    def test_f_0(self):
        n = f_s("f_0_test.txt")
        self.assertEqual(f_0_v("f_0_test.txt"), n)
    # 1st frequency moment
    def test_f_1(self):
        f_1 = f_1_test("f_1_test.txt")
        self.assertEqual(f_1_v("f_1_test.txt"), f_1)
    # 2nd frequency moment
    def good_h(self):
        k = 45
        n = 10
        s = [10,2,10,10,10,10,10,10,10,10]
        q, r, h, v_sketch = sketch_2d("known_f_2.txt", k)
        h_2d_t("known_f_2_h.txt", n, s, q)
        f_2 = verify(v_sketch, "known_f_2_h.txt", g.GF(q), r, h)
        self.assertEqual(f_2, 904)
    def bad_h(self):
        k = 45
        n = 10
        s = [10,2,10,10,10,10,10,10,10,10]
        q, r, h, v_sketch = sketch_2d("known_f_2.txt", k)
        h = h_2d_f("known_f_2_h.txt", n, s, q)
        h = np.random.permutation(h)
        f_2 = verify(v_sketch, "known_f_2_h.txt", g.GF(q), r, h)
        self.assertFalse(f_2)
    def honest(self):
        k = 45
        n, s = f_2_s("f_2_h_test.txt")
        f_2 = [s_i**2 for s_i in s]
        q, r, h, v_sketch = sketch_2d("known_f_2.txt", k)
        h_2d_t("known_f_2_h.txt", n, s, q)
        f_2 = verify(v_sketch, "known_f_2_h.txt", g.GF(q), r, h)
        self.assertEqual(f_2, f_2)
    def dishonest(self):
        k = 45
        n, s = f_2_s("f_2_h_test.txt")
        f_2 = [s_i**2 for s_i in s]
        q, r, h, v_sketch = sketch_2d("known_f_2.txt", k)
        h_2d_f("known_f_2_h.txt", n, s, q)
        f_2 = verify(v_sketch, "known_f_2_h.txt", g.GF(q), r, h)
        self.assertFalse(f_2)

