# naive ZK index : assumes honest verifier
# multivariate 

# input: the length of the stream a, the stream a, the index j
# output: the jth element of a
import math
import numpy as np
import secrets
import galois as g
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from stream_generation.gen_index import gen_zk_index
from equality import stream_generator
from index_multivariate import m_compute_g, interpolate_p, precomp_denominators, line_vals, compute_basis

# we start with a consisting of a_1 to a_n
# we create the l(x,r) line 
# for non zk we would just send f evaluated at all the points f_{a_1}, ... f_{a_n} 

def zk_index_h(filename, dim):
    q = 65537
    # create the stream
    a = gen_zk_index(filename)
    #verifer creates its sketch
    F_q, mu, r, mapped_r, sketch, n, h, a_j = h_verifier(filename, q, dim, r)
    # prover calculates the g vals
    g = m_compute_g(a, a_j, mu, mapped_r, n, h, F_q, dim)
    # algebraic commitment
    p = secrets.randbelow(1000)
    g_0, commit, deg_g = algebraic_commitment(g, F_q, p)
    y, gamma, k = commit
    folded_gamma, fp, beta = fingerprint(r, y, gamma, k, deg_g, F_q)
    # algebraic decommitment
    unlocked_evals = algebraic_decommitment(y,k) 
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g_zk(folded_gamma, unlocked_evals, beta, g_0, fp, mu, sketch, gamma, F_q)

def zk_index_d_prover(filename, dim):
    q = 65537
    # create the stream
    a = gen_zk_index(filename)
    #verifer creates its sketch
    F_q, mu, r, mapped_r, sketch, n, h, a_j = h_verifier(filename, q, dim, r)
    # prover calculates the g vals
    g = m_compute_g(a, a_j, mu, mapped_r, n, h, F_q, dim)
    # algebraic commitment
    p = secrets.randbelow(1000)
    g_0, commit, deg_g = algebraic_commitment(g, F_q, p)
    y, gamma, k = commit
    folded_gamma, fp, beta = fingerprint(r, y, gamma, k, deg_g, F_q)
    unlocked_evals = algebraic_decommitment(y,k) 
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g_zk(folded_gamma, unlocked_evals, beta, g_0, fp, mu, sketch, gamma, F_q)

def perm_F_q(q):
    perm = np.random.permutation(np.arange(q))
    return perm
        
# honest verifier
def h_verifier(filename, q, dim, r):
    # input is the length of stream a, the stream a and the index j
    stream = stream_generator(filename)
    # n: length of the input without annotation
    n = next(stream)
    h = math.ceil(math.pow(n, 1/dim))
    # F_q: field for the low degree extension
    F_q = g.GF(q)
    shape = [h] * dim
    mapped_r = tuple(F_q((r + i) % q) for i in range(dim))
    # mu: non-zero element of F_q
    mu = F_q(secrets.randbelow(q-2)+1)
    # precompute stage
    numerators = F_q.Zeros(dim)
    denominators = F_q.Zeros(dim)
    precomp = F_q.Ones((dim,h))
    for dimension in range(dim):
        numerators[dimension] = F_q(1)
        for i in range(h):
            numerators[dimension] *= mapped_r[dimension] - F_q(i)
        precomp[dimension] = F_q.Ones(h)
        for a in range(h):
            denominators[dimension] = (math.factorial(a) * ((-1) ** (h-1-a)) * math.factorial(h-1-a)) % q
            precomp[dimension][a] = numerators[dimension] / ((mapped_r[dimension] - F_q(a)) * denominators[dimension])
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
    return (F_q, mu, r, mapped_r, sketch, n, h, a_j)

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

# prover       
def algebraic_commitment(g_vals, F_q, p):
    # L(0) = j, this is sent without padding 
    x_j = g_vals[0]
    locked_vals = F_q(g_vals[1:])
    deg_g = len(locked_vals)
    y = F_q.Random((deg_g, p))
    k = secrets.randbelow(p)
    gamma = locked_vals - y[:,k]
    return x_j, (y, gamma, k), deg_g

# verifier
def fingerprint(rho, y, gamma, k, deg_g, F_q):
    d_inv, grid = precomp_denominators(deg_g, F_q)
    beta = compute_basis(deg_g, F_q, F_q(rho), d_inv, grid)
    folded_gamma = np.dot(beta, gamma)
    sigma = secrets.randbelow(F_q.order)
    folded_y = np.dot(beta, y)
    fingerprint = interpolate_p(folded_y, sigma, F_q)
    return folded_gamma, fingerprint, beta

# prover
def algebraic_decommitment(y, k):
    unlocked_evals = y[:,k]
    return unlocked_evals

# verifier 
def check_g_zk(folded_gamma, g_evals, beta, x_j, fp, mu, sketch, gamma, F_q):
    # TODO : check fingerprint  
    locked_vals = gamma + g_evals
    full_evals = F_q([x_j] + locked_vals.tolist())
    g_mu = interpolate_p(full_evals, mu, F_q)
    if g_mu == sketch:
        return int(x_j)
    else:
        print("Algebraic Commitment failed.")
        return False
    