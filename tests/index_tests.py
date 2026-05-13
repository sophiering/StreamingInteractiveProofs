#non_zk_index_tests
import unittest
import numpy as np
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))


from stream_generation.gen_index import fixed_test, index_test, index_eval
from protocols.index import verifier, compute_g, check_g
from protocols.index_multivariate import m_verifier, m_compute_g, m_check_g

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
        g = m_compute_g(a, a_j, mu, r, n, h, F_q, 3)
        self.assertEqual(m_check_g(sketch, g, mu, F_q), true_a_j)
    def multivariate_d(self):
        filename = "multivariate_3d.txt"
        a, true_a_j = index_test(filename)
        F_q, mu, r, sketch, n, h, a_j = m_verifier(filename, 3)
        g = m_compute_g(a, a_j, mu, r, n, h, F_q, 3)
        self.assertEqual(m_check_g(sketch, g, mu, F_q), true_a_j)
    

