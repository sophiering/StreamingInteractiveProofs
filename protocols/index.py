# non ZK index 

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

# larger k = more accuracy
k = 45

# for bivariate:
# a_j = tuple x_j (a,b)
# r = tuple r (c,d)

# works!
def index_t(filename):
    # create the stream
    a = gen_index(filename)
    #verifer creates its sketch
    F_q, mu, r, sketch, n, h, a_j = verifier(filename)
    # prover calculates the g vals
    g = compute_g(a, a_j, mu, r, n, h, F_q)
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g(sketch, g, mu, F_q)

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
def verifier(filename):
    stream = stream_generator(filename)
    # input is the length of stream a, the stream a and the index j
    k = 45
    # n: length of the input without annotation
    n = next(stream)
    h = math.ceil(math.sqrt(n))
    # m = n + random.randint(1,100000)
    # qmin = max(pow(m, k), 3*k*h)
    # q = pick_prime(qmin,k)
    q = 2305843009213693951
    # F_q: field for the low degree extension
    F_q = g.GF(q)
    # mu: non-zero element of F_q
    mu = F_q(random.randint(1,q-1))
    # r: random point r (r_i,r_j) that the line will pass through alongside j
    r = [F_q(secrets.randbelow(q)), F_q(secrets.randbelow(q))]
    # precompute stage
    # precompute rows
    numerator_rows = F_q(1)
    for i in range(h):
        numerator_rows *= (r[0] - F_q(i))
    precomp_rows = F_q.Ones(h)
    for a in range(h):
        denominator_rows = math.factorial(a) * ((-1) ** (h-1-a)) * math.factorial(h-1-a)
        denominator_rows = F_q(denominator_rows % q)
        precomp_rows[a] = numerator_rows / ((r[0] - F_q(a)) * denominator_rows)
    # precompute columns
    numerator_cols = F_q(1)
    for i in range(h):
        numerator_cols *= (r[1] - F_q(i))
    precomp_cols = F_q.Ones(h)
    for a in range(h):
        denominator_cols = math.factorial(a) * ((-1) ** (h-1-a)) * math.factorial(h-1-a)
        denominator_cols = F_q(denominator_cols % q)
        precomp_cols[a] = numerator_cols / ((r[1] - F_q(a)) * denominator_cols)
    # create sketch for r
    sketch = F_q(0)
    for i in range(n):
        a_i = next(stream)
        # map linear index to 2D coordinates (s_a, s_b)
        s_a = i // h
        s_b = i % h
        sketch += a_i * precomp_rows[s_a] * precomp_cols[s_b]
    # index of 
    j = next(stream)
    a_j = (F_q(j //h), F_q(j % h))
    if n < j:
        return False
    # check with prover
    return (F_q, mu, r, sketch, n, h, a_j)

# compute g
def line_vals(a_j, t, mu, r):
    l_x = a_j[0] + (t / mu) * (r[0] - a_j[0])
    l_y = a_j[1] + (t / mu) * (r[1] - a_j[1])
    return (l_x, l_y)

# compute g
def compute_basis(h, F_q, target):
    # edge case
    for i in range(h):
        if target == F_q(i):
            basis = [F_q(0)] * h
            basis[i] = F_q(1)
            return basis
    # majority case
    numerator = F_q(1)
    for i in range(h):
        numerator *= (target - F_q(i))
    basis = [F_q(0)] * h
    q = F_q.order
    for j in range(h):
        denominator = math.factorial(j) * ((-1) ** (h-1-j)) * math.factorial(h-1-j)
        F_q_denominator = F_q(denominator % q)
        basis[j] = numerator / ((target - F_q(j)) * F_q_denominator)
    return basis

# prover
def compute_g(a, a_j, mu, r, n, h, F_q):
    degree = 2 * h - 2
    g_vals = []
    padded_a = list(a) + [0] * ((h*h) - n)
    matrix = [padded_a[i:i + h] for i in range(0, h*h, h)]
    F_q_matrix = F_q(matrix)
    for t in range(degree + 1):
        t_f = F_q(t)
        x, y = line_vals(a_j, t_f, mu, r)
        row_basis = F_q(compute_basis(h, F_q, x))
        col_basis = F_q(compute_basis(h, F_q, y))
        #compute P(x,y)
        t_val = F_q(0)
        t_val = row_basis @ F_q_matrix @ col_basis
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
    






