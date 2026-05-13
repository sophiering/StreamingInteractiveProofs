# multivariate index 

# input: the length of the stream a, the stream a, the index j
# output: the jth element of a
import math
import secrets
import numpy as np
import galois as g
import sys
from pathlib import Path
from functools import reduce

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.equality import pick_prime, stream_generator
from stream_generation.gen_index import gen_index

# works!
def index_t(filename, dim):
    # create the stream
    a = gen_index(filename)
    #verifer creates its sketch
    F_q, mu, r, sketch, n, h, a_j = m_verifier(filename, dim)
    # prover calculates the g vals
    g = m_compute_g(a, a_j, mu, r, n, h, F_q, dim)
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return m_check_g(sketch, g, mu, F_q)

def index_f(filename, dim):
    # create the stream
    a = gen_index(filename)
    #verifer creates its sketch
    F_q, mu, r, sketch, n, h, a_j = m_verifier(filename, dim)
    # prover calculates the INCORRECT g vals
    g = m_compute_g(a, a_j, mu, r, n, h, F_q, dim)
    g = np.random.permutation(g)
    g[0] += 1
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return m_check_g(sketch, g, mu, F_q)

# verifier
def m_verifier(filename, dim):
    # input is the length of stream a, the stream a and the index j
    stream = stream_generator(filename)
    # n: length of the input without annotation
    n = next(stream)
    h = math.ceil(math.pow(n, 1/dim))
    shape = [h] * dim
    q = 2147483647
    # F_q: field for the low degree extension
    F_q = g.GF(q)
    # mu: non-zero element of F_q
    mu = F_q(secrets.randbelow(q-2)+1)
    # r: random point r (r_i,r_j) that the line will pass through alongside j
    r = F_q([secrets.randbelow(q) for _ in range(dim)])
    # precompute stage
    numerators = F_q.Zeros(dim)
    denominators = F_q.Zeros(dim)
    precomp = F_q.Ones((dim,h))
    for dimension in range(dim):
        numerators[dimension] = F_q(1)
        for i in range(h):
            numerators[dimension] *= r[dimension] - F_q(i)
        precomp[dimension] = F_q.Ones(h)
        for a in range(h):
            denominators[dimension] = (math.factorial(a) * ((-1) ** (h-1-a)) * math.factorial(h-1-a)) % q
            precomp[dimension][a] = numerators[dimension] / ((r[dimension] - F_q(a)) * denominators[dimension])
    # create sketch for r
    sketch = F_q(0)
    for i in range(n):
        # map 1D index to kD coordinates 
        a_i = next(stream)
        s = np.unravel_index(i,shape)
        total = 1
        for dimension in range(dim):
            total *= precomp[dimension][s[dimension]] 
        sketch += a_i * total
    # index of 
    j = next(stream)
    a_j = np.unravel_index(j,shape)
    if n < j:
        return False
    # check with prover
    return (F_q, mu, r, sketch, n, h, a_j)

# prover: compute g
def line_vals(a_j, t, mu, r, F_q, dim):
    l = F_q.Zeros(dim)
    for dimension in range(dim):
        F_q_a_j = F_q(a_j[dimension])
        l[dimension] = F_q_a_j + (t / mu) * (r[dimension] - F_q_a_j)
    return l

# prover: compute g 
def precomp_denominators(h, F_q):
    denominators = [F_q(0)] * h
    q = F_q.order
    for j in range(h):
        denominator = math.factorial(j) * ((-1) ** (h-1-j)) * math.factorial(h-1-j)
        denominators[j] = F_q(denominator % q)
    d_arr = F_q(denominators)
    # removes the repeated finite field division later on
    d_inv = F_q(1) / d_arr
    grid = F_q(np.arange(h))
    return d_inv, grid

# prover: compute g
def compute_basis(h, F_q, target, d_inv, grid):
    target_int = int(target)
    # edge case
    if target_int < h:
        basis = F_q.Zeros(h)
        basis[target_int] = F_q(1)
        return basis
    # majority case
    diffs = target - grid
    numerator = np.prod(diffs)
    basis = numerator * d_inv / diffs
    return basis

# prover
def m_compute_g(a, a_j, mu, r, n, h, F_q, dim):
    d_inv, grid = precomp_denominators(h, F_q)
    degree = dim * (h - 1)
    g_vals = []
    F_a = F_q(a)
    # do we need to make a F_q(a)? 
    for t in range(degree + 1):
        t_f = F_q(t)
        l = line_vals(a_j, t_f, mu, r, F_q, dim)
        bases = []
        # precompute basis weights
        for d in range(dim):
            bases.append(compute_basis(h, F_q, l[d], d_inv, grid))
        weight = bases[0]
        # outer product for multivariate basis weights (lagrange polynomial value at t)
        for b in bases[1:]:
            weight = np.outer(weight,b)
        # compute P(x,y)
        t_val = F_q(0)
        current_weight = weight.flatten()[:n]
        t_val = F_a @ current_weight
        g_vals.append(t_val)
    # return : coefficients polynomial g, where g(0) = x_j and g(mu) = r
    return g_vals

# check g 
def interpolate_p(g, target, F_q):
    target = F_q(target)
    d = len(g) - 1
    # edge case
    for i in range(d+1):
        if target == F_q(i):
            return g[i]
    # majority case
    result = F_q(0)
    numerator = F_q(1)
    for i in range(d+1):
        numerator *= (target - F_q(i))
    q = F_q.order
    for j in range(d+1):
        denominator = math.factorial(j) * ((-1) ** (d-j)) * math.factorial(d-j)
        F_q_denominator = F_q(denominator % q)
        basis_weight = numerator / ((target - F_q(j)) * F_q_denominator)
        result += g[j] * basis_weight
    return result

# verifier 
def m_check_g(sketch, g, mu, F_q):
    g_mu = interpolate_p(g, mu, F_q)
    # if initial sketch for r == g(mu) 
    if g_mu == sketch:
    # compute g(0)
        a_j_val = interpolate_p(g, 0, F_q)
        print(a_j_val)
        return a_j_val
    # else throw error
    else:
        print(False)
        return False
    

    