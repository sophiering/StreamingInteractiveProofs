#non_zk_index_tests
import unittest
import numpy as np
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))


from stream_generation.gen_index import fixed_test, index_test, index_eval
from protocols.index import verifier, compute_g, check_g
from protocols.index_multivariate import m_verifier, HonestProver, DishonestProver, m_check_g
from protocols.honest_v_zk_index import honest_zk_h_p, honest_zk_d_p
from protocols.zk_index import zk_h_test, zk_d_p_test, zk_d_v_test

class TestClass(unittest.TestCase):
    def honest(self):
        filename = "input1.txt"
        a, true_a_j = index_test(filename)
        F_q, mu, r, sketch, n, h, a_j = verifier(filename)
        g = compute_g(a, a_j, mu, r, n, h, F_q)
        self.assertEqual(check_g(sketch, g, mu, F_q), true_a_j)
    def dishonest(self):
        filename = "input1.txt"
        a, _ = index_test(filename)
        F_q, mu, r, sketch, n, h, a_j = verifier(filename)
        g = compute_g(a, a_j, mu, r, n, h, F_q)
        g = np.random.permutation(g)
        self.assertFalse(check_g(sketch, g, mu, F_q))
    def multivariate_h(self):
        filename = "multivariate_3d.txt"
        a, true_a_j = index_test(filename)
        F_q, mu, r, sketch, n, h, a_j = m_verifier(filename, 3)
        prover = HonestProver(a, a_j, n, h, F_q, 3)
        g = prover.compute_g(mu, r)
        self.assertEqual(m_check_g(sketch, g, mu, F_q), true_a_j)
    def multivariate_d(self):
        filename = "multivariate_3d.txt"
        a, true_a_j = index_test(filename)
        F_q, mu, r, sketch, n, h, a_j = m_verifier(filename, 3)
        prover = DishonestProver(a, a_j, n, h, F_q, 3)
        g = prover.compute_g(mu, r)
        self.assertEqual(m_check_g(sketch, g, mu, F_q), true_a_j)
    def h_v_zk_h_p(self):
        filename = "honest_zk_3d.txt"
        a, true_a_j = index_test(filename)
        self.assertEqual(honest_zk_h_p(filename, 3, a), true_a_j)
    def h_v_zk_d_p(self):
        filename = "honest_zk_3d.txt"
        a, _ = index_test(filename)
        self.assertFalse(honest_zk_d_p(filename, 3, a))
    def zk_h(self):
        filename = "zk_3d.txt"
        a, true_a_j = index_test(filename)
        self.assertEqual(zk_h_test(filename, 3, a), true_a_j)
    def zk_d_p(self):
        filename = "zk_3d.txt"
        a, _ = index_test(filename)
        self.assertFalse(zk_d_p_test(filename, 3, a))
    def zk_d_v(self):
        filename = "multivariate_3d.txt"
        a, _ = index_test(filename)
        self.assertFalse(zk_d_v_test(filename, 3, a))
    

