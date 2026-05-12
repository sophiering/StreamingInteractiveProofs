# multivariate index 

# input: the length of the stream a, the stream a, the index j
# output: the jth element of a
import math
import random
import secrets
import numpy as np
import galois as g
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.equality import pick_prime, stream_generator
from stream_generation.gen_index import gen_index

# for bivariate:
# a_j = tuple x_j (a,b)
# r = tuple r (c,d)

# works!
def index_t(filename, dim):
    # create the stream
    a = gen_index(filename)
    #verifer creates its sketch
    F_q, mu, r, sketch, n, h, a_j = verifier(filename, dim)
    # prover calculates the g vals
    g = compute_g(a, a_j, mu, r, n, h, F_q, dim)
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g(sketch, g, mu, F_q, dim)

def index_f(filename):
    # create the stream
    a = gen_index(filename)
    #verifer creates its sketch
    F_q, mu, r, sketch, n, h, a_j = verifier(filename)
    # prover calculates the g vals
    g = compute_g(a, a_j, mu, r, n, h, F_q)
    g = np.random.permutation(g)
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g(sketch, g, mu, F_q)

# verifier
def verifier(filename, dim):
    # input is the length of stream a, the stream a and the index j
    stream = stream_generator(filename)
    # larger k = more accuracy
    k = 45
    # n: length of the input without annotation
    n = next(stream)
    h = math.ceil(math.pow(n, 1/dim))
    shape = [h] * dim
    # m = n + random.randint(1,100000)
    # qmin = max(pow(m, k), 3*k*h)
    # q = pick_prime(qmin,k)
    q = 2305843009213693951
    # F_q: field for the low degree extension
    F_q = g.GF(q)
    # mu: non-zero element of F_q
    mu = F_q(random.randint(1,q-1))
    # r: random point r (r_i,r_j) that the line will pass through alongside j
    r = [F_q(secrets.randbelow(q))] * dim
    # precompute stage
    numerators = np.zeros(dim)
    denominators = np.zeros(dim)
    precomp = np.ones((dim,h))
    for dimension in dim:
        numerators[dimension] = F_q(1)
        for i in range(h):
            numerators[dimension] *= (r[dimension] - F_q(i))
        precomp[dim] = F_q.Ones(h)
        for a in range(h):
            denominators[dimension] = math.factorial(a) * ((-1) ** (h-1-a)) * math.factorial(h-1-a)
            denominators[dimension] = F_q(denominators[dimension] % q)
            precomp[a] = numerators[dimension] / ((r[dimension] - F_q(a)) * denominators[dimension])
    # create sketch for r
    sketch = F_q(0)
    for i in range(n):
        # map 1D index to kD coordinates 
        a_i = next(stream)
        s = np.unravel_index(i,shape)
        total = 1
        for dimension in dim:
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
def line_vals(a_j, t, mu, r, dim):
    l = np.zeros(dim)
    for dimension in dim:
        l[dimension] = a_j[dimension] + (t / mu) * (r[dimension] - a_j[dimension])
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
def compute_g(a, a_j, mu, r, n, h, F_q, dim):
    degree = dim * (h - 1)
    g_vals = []
    padded_a = list(a) + [0] * ((h*h) - n)
    for t in range(degree + 1):
        t_f = F_q(t)
        l = line_vals(a_j, t_f, mu, r, dim)
        bases = []
        for d in range(dim):
            bases.append(compute_basis(h, F_q, l[d]))
        # compute P(x,y)
        for i in range
        t_val = F_q(0)
        t_val = d_basis @ F_q_matrix 
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
def check_g(sketch, g, mu, F_q):
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