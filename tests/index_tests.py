#non_zk_index_tests
import unittest
import numpy as np
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))


from stream_generation.gen_index import fixed_test, index_test
from protocols.index import verifier, compute_g, check_g

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
        self.assertEqual(check_g(sketch, g, mu, F_q), False)

