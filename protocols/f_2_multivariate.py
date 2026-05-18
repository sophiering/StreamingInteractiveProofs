# multivariate frequency moments: F_2
# input: length of stream a, the stream a, the helper's annotation
# output: the frequency moment 
import math
import random
import numpy as np
import galois as g
import secrets
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from stream_generation.gen_freq_moments import f_2_s
from protocols.equality import stream_generator

def m_f_2_h(filename, dim):
    q = 2147483647
    # f_2_s(filename)
    F_q, r_challenges, h, f_eval = m_create_sketch(filename, dim)
    #proof_polynomials, _ = m_h_prover(filename, dim, q, r_challenges)
    prover = HonestProver(filename, dim, F_q)
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
    return final_check(expected_sum, f_eval, claimed_f_2)

def m_f_2_d(filename, dim):
    q = 2147483647
    # f_2_s(filename)
    F_q, r_challenges, h, f_eval = m_create_sketch(filename, dim)
    #proof_polynomials, _ = m_h_prover(filename, dim, q, r_challenges)
    prover = DishonestProver(filename, dim, F_q)
    expected_sum = None
    claimed_f_2 = None
    # k rounds of sum check
    for k in range(dim):
        P_k = prover.gen_polynomial(F_q)
        result = verify_round(P_k, F_q, r_challenges[k], h, expected_sum)
        if result == False:
            return False
        expected_sum, actual_sum = result
        if k == 0:
            claimed_f_2 = actual_sum
        prover.reply(r_challenges[k])
    return final_check(expected_sum, f_eval, claimed_f_2)

def m_create_sketch(filename, dim):
    filepath = base_path / "streams" / filename
    # input is the elements followed by the helper's annotation: a_1, ... a_n, s'(x)
    stream = stream_generator(filepath)
    # length of the input without annotation
    n = next(stream) 
    m = n + random.randint(1,100000)
    h = math.ceil(math.pow(n, 1/dim))
    shape = [h] * dim
    q = 2147483647
    F_q = g.GF(q)
    r = F_q([secrets.randbelow(q) for _ in range(dim)])
    # precompute 
    precomp = F_q.Ones((dim,h))
    for dimension in range(dim):
        for a in range(h):
            num = F_q(1)
            denom = F_q(1)
            for i in range(h):
                if i != a:
                    num *= r[dimension] - F_q(i)
                    denom *= F_q(a) - F_q(i)
            precomp[dimension][a] *= num / denom     
    # create the h x v matrix
    f_eval = F_q(0)
    for item in range(n):
        # map to 3D coordinates (s_a, s_b, s_c)
        value = next(stream)
        current_value = F_q(value)
        k_dim_v = np.unravel_index(item, shape)
        total = F_q(1)
        for dimension in range(dim):
            total *= precomp[dimension,k_dim_v[dimension]]
        f_eval += current_value * total
    return F_q, r, h, f_eval

# precompute lagrange at eval points
def precompute_lagrange(F_q, eval_points, h):
    m = F_q.Zeros((len(eval_points), h), dtype=np.int64)
    for i, x_val in enumerate(eval_points):
        for a in range(h):
            if x_val == F_q(a):
                m[i, a] = F_q(1)
            else:
                num = F_q(1)
                denom = F_q(1)
                for j in range(h):
                    if j != a:
                        num *= (x_val - F_q(j))
                        denom *= (F_q(a) - F_q(j))
                m[i, a] = num / denom
    return m

# honest prover class
class HonestProver:
    def __init__(self, filename, dim, F_q):
        self.F_q = F_q
        self.dim = dim
        self.k = 0
        stream = stream_generator(filename)
        n = next(stream)
        self.h = math.ceil(math.pow(n, 1/dim))
        # degree of each polynomial
        s_padded = np.zeros(self.h**dim, dtype=np.int64)
        self.degree = 2 * (self.h - 1)
        for i in range(n):
            s_padded[i] = next(stream)
        # shape into a k-dimensional hypercube
        self.grid = self.F_q(s_padded).reshape((self.h,) * dim)
        # the d + 1 points needed to define polynomial 
        self.eval_points = [F_q(i) for i in range(self.degree + 1)]
        self.precompute_eval = precompute_lagrange(F_q, self.eval_points, self.h)
    
    def gen_polynomial(self):
        grid_2d = self.grid.reshape((self.h, -1))
        f_tilde = np.matmul(self.precompute_eval, grid_2d)
        s_prime = np.sum(f_tilde ** 2, axis=1)
        return s_prime
    
    def reply(self, r_k):
        grid_2d = self.grid.reshape((self.h, -1))
        precompute_fold = precompute_lagrange(self.F_q, [r_k], self.h)
        grid_flat = np.matmul(precompute_fold, grid_2d)[0]
        if self.k < (self.dim - 1):
            self.grid = grid_flat.reshape((self.h,) * (self.dim - self.k - 1))
        else:
            self.grid = grid_flat
        self.k += 1

# dishonest prover class
class DishonestProver:
    def __init__(self, filename, dim, F_q):
        self.F_q = F_q
        self.dim = dim
        self.k = 0
        stream = stream_generator(filename)
        n = next(stream)
        self.h = math.ceil(math.pow(n, 1/dim))
        # degree of each polynomial
        s_padded = np.zeros(self.h**dim, dtype=np.int64)
        self.degree = 2 * (self.h - 1)
        for i in range(n):
            s_padded[i] = next(stream)
        # shape into a k-dimensional hypercube
        self.grid = self.F_q(s_padded).reshape((self.h,) * dim)
        # the d + 1 points needed to define polynomial 
        self.eval_points = [F_q(i) for i in range(self.degree + 1)]
        self.precompute_eval = precompute_lagrange(F_q, self.eval_points, self.h)
    
    def gen_polynomial(self, F_q):
        grid_2d = self.grid.reshape((self.h, -1))
        f_tilde = np.matmul(self.precompute_eval, grid_2d)
        s_prime = np.sum(f_tilde ** 2, axis=1)
        # maliciously alter s prime
        s_prime += F_q(1)
        return s_prime
    
    def reply(self, r_k):
        grid_2d = self.grid.reshape((self.h, -1))
        precompute_fold = precompute_lagrange(self.F_q, [r_k], self.h)
        grid_flat = np.matmul(precompute_fold, grid_2d)[0]
        if self.k < (self.dim - 1):
            self.grid = grid_flat.reshape((self.h,) * (self.dim - self.k - 1))
        else:
            self.grid = grid_flat
        self.k += 1

def interpolate_at_point(polynomial_evals, point, F_q):
    d = len(polynomial_evals) - 1
    total = F_q(0)
    for X in range(d + 1):
        num = F_q(1)
        den = F_q(1)
        for i in range(d + 1):
            if i != X:
                num *= (point - F_q(i))
                den *= (F_q(X) - F_q(i))
        total += polynomial_evals[X] * (num / den)
    return total

def verify_round(proof_polynomial, F_q, r_k, h, expected_sum):
    # calculate prover's claimed f_2 by summing the first polynomial over the k dimensions
    P_k = F_q(proof_polynomial)
    actual_sum = F_q(0)
    for x in range(h):
        actual_sum += P_k[x]
    if (expected_sum is not None) and (actual_sum != expected_sum):
        print("sum-check fail")
        return False
    expected_sum = interpolate_at_point(P_k, r_k, F_q)
    return expected_sum, actual_sum


    # final check 
def final_check(expected_sum, f_eval_from_sketch, claimed_f_2):
    if expected_sum != (f_eval_from_sketch ** 2):
        print("malicious prover deteched :(")
        return False
    return int(claimed_f_2)
