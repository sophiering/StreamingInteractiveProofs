# frequency moments tests
import unittest
import sys
import numpy as np
import galois as g
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from stream_generation.gen_freq_moments import f_s, f_1_test, f_2_s, f_2_eval
from protocols.freq_moments import f_0_v, f_1_v, sketch_2d, h_2d_t, h_2d_f, verify
from protocols.f_2_multivariate import m_create_sketch, verify_round, final_check, HonestProver, DishonestProver

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
        h_array = h_2d_f("known_f_2_h.txt", n, s, q)
        F_q = g.GF(q)
        h_array[0] += F_q(1)
        with open("known_f_2_h.txt", "w") as f:
            for val in h_array:
                f.write(f"{int(val)}\n")
        f_2 = verify(v_sketch, "known_f_2_h.txt", F_q, r, h)
        self.assertFalse(f_2)
    def honest(self):
        k = 45
        n, s = f_2_s("f_2_h_test.txt")
        true_f_2 = [s_i**2 for s_i in s]
        q, r, h, v_sketch = sketch_2d("known_f_2.txt", k)
        h_2d_t("known_f_2_h.txt", n, s, q)
        f_2 = verify(v_sketch, "known_f_2_h.txt", g.GF(q), r, h)
        self.assertEqual(f_2, true_f_2)
    def dishonest(self):
        k = 45
        n, s = f_2_s("f_2_h_test.txt")
        true_f_2 = [s_i**2 for s_i in s]
        q, r, h, v_sketch = sketch_2d("known_f_2.txt", k)
        h_2d_f("known_f_2_h.txt", n, s, q)
        f_2 = verify(v_sketch, "known_f_2_h.txt", g.GF(q), r, h)
        self.assertFalse(f_2)
    def f_2_3d_t(self):
        dim = 3
        s = f_2_eval("f_2_3d.txt", 1000)
        true_f_2 = sum((s_i**2 % 2147483647) for s_i in s) % 2147483647
        F_q, r_challenges, h, f_eval = m_create_sketch("f_2_3d.txt", dim)
        prover = HonestProver("f_2_3d.txt", dim, F_q)
        expected_sum = None
        claimed_f_2 = None
        # k rounds of sum check
        for k in range(dim):
            P_k = prover.gen_polynomial()
            result = verify_round(P_k, F_q, r_challenges[k], h, expected_sum)
            if result == False:
                return False
            expected_sum, actual_sum = result
            if k == 0:
                claimed_f_2 = actual_sum
            prover.reply(r_challenges[k])
        self.assertEqual(final_check(expected_sum, f_eval, claimed_f_2), true_f_2)
    def f_2_3d_f(self):
        dim = 3
        s = f_2_eval("f_2_3d.txt", 1000)
        F_q, r_challenges, h, f_eval = m_create_sketch("f_2_3d.txt", dim)
        prover = DishonestProver("f_2_3d.txt", dim, F_q)
        expected_sum = None
        claimed_f_2 = None
        # see if verifier can identify malicious prover
        protocol = True
        # k rounds of sum check
        for k in range(dim):
            P_k = prover.gen_polynomial(F_q)
            result = verify_round(P_k, F_q, r_challenges[k], h, expected_sum)
            if result == False:
                protocol = False
                break
            expected_sum, actual_sum = result
            if k == 0:
                claimed_f_2 = actual_sum
            prover.reply(r_challenges[k])
            if protocol:
                protocol = final_check(expected_sum, f_eval, claimed_f_2)
        self.assertFalse(protocol)

