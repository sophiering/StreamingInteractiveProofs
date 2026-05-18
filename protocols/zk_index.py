# strong ZK index
# ZK multivariate index: extend to 3D (trivariate) vs 2D (bivariate)

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

from stream_generation.gen_index import gen_index
from protocols.equality import stream_generator
from protocols.index_multivariate import precomp_denominators, line_vals, compute_basis
from protocols.honest_v_zk_index import algebraic_commitment, fingerprint, check_g_zk

# we start with a consisting of a_1 to a_n
# we create the l(x,r) line 
# for non zk we would just send f evaluated at all the points f_{a_1}, ... f_{a_n} 

def zk_index_h(filename, dim):
    q = 65537
    # create the stream
    # a = gen_index(filename)
    prover = ZKHonestProver(a, dim, q)
    # send perm F_q
    perm = prover.perm_F_q()
    # verifier temporal commitment
    r, index = temporal_commitment(perm, q)
    #verifer creates its sketch
    F_q, mu, r, mapped_r, sketch, n, h, a_j = h_verifier(filename, q, dim, r)
    # prover observe
    prover.observe(a_j, n, h, F_q)
    # algebraic commitment
    p = 100 + secrets.randbelow(1000)
    # prover calculates the g vals
    g_0, commit, deg_g = prover.compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    # temporal decommitment
    if temporal_decommitment(perm, r, index) == False:
        return False
    # algebraic decommitment
    unlocked_evals = prover.algebraic_decommitment(y,k) 
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g_zk(F_q, mu, sketch, g_0, gamma, k, unlocked_evals, folded_gamma, fp, beta, folded_y, sigma)

def zk_index_d_prover(filename, dim):    
    q = 65537
    # create the stream
    # a = gen_index(filename)
    prover = ZKDishonestProver(a, dim, q)
    # send perm F_q
    perm = prover.perm_F_q()
    # verifier temporal commitment
    r, index = temporal_commitment(perm, q)
    #verifer creates its sketch
    F_q, mu, r, mapped_r, sketch, n, h, a_j = h_verifier(filename, q, dim, r)
    # prover observe
    prover.observe(a_j, n, h, F_q)
    # algebraic commitment
    p = 100 + secrets.randbelow(1000)
    # prover calculates the g vals
    g_0, commit, deg_g = prover.compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    # temporal decommitment
    if temporal_decommitment(perm, r, index) == False:
        return False
    # algebraic decommitment
    unlocked_evals = prover.algebraic_decommitment(y,k) 
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g_zk(F_q, mu, sketch, g_0, gamma, k, unlocked_evals, folded_gamma, fp, beta, folded_y, sigma)

def zk_index_d_verifier(filename, dim):
    q = 65537
    # create the stream
    # a = gen_index(filename)
    prover = ZKHonestProver(a, dim, q)
    # send perm F_q
    perm = prover.perm_F_q()
    # verifier temporal commitment
    temporal_commitment(perm, q)
    #verifer creates its sketch of big ole nothing
    F_q, mu, r, mapped_r, sketch, n, h, a_j, index = d_verifier(filename, q, dim)
    # prover observe
    prover.observe(a_j, n, h, F_q)
    # algebraic commitment
    p = 100 + secrets.randbelow(1000)
    # prover calculates the g vals
    g_0, commit, deg_g = prover.compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    # temporal decommitment
    if temporal_decommitment(perm, r, index) == False:
        print("malicious verifier")
        return False
    # algebraic decommitment
    unlocked_evals = prover.algebraic_decommitment(y,k) 
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g_zk(F_q, mu, sketch, g_0, gamma, k, unlocked_evals, folded_gamma, fp, beta, folded_y, sigma)

def temporal_commitment(perm, q):
    r = secrets.randbelow(q)
    for i, val in enumerate(perm):
        if val == r:
            return r, i
        
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

# dishonest verifier
def d_verifier(filename, q, dim):
    # input is the length of stream a, the stream a and the index j
    stream = stream_generator(filename)
    # larger k = more accuracy
    k = 45
    # n: length of the input without annotation
    n = next(stream)
    h = math.ceil(math.pow(n, 1/dim))
    shape = [h] * dim
    # F_q: field for the low degree extension
    F_q = g.GF(q)
    # mu: non-zero element of F_q
    mu = F_q(secrets.randbelow(q-2)+1)
    # ignores the input stream
    for _ in range(n):
        next(stream)
    # index of 
    j = next(stream)
    a_j = np.unravel_index(j,shape)
    # maliciously choses r to learn more than necessary
    r = j + 1 
    mapped_r = tuple(F_q((r + i) % q) for i in range(dim))
    # must guess index
    index = secrets.randbelow(q)
    # check with prover
    return (F_q, mu, r, mapped_r, F_q(0), n, h, a_j, index)

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
def temporal_decommitment(perm, r, index):
    if perm[index] == r:
        return True
    else:
        return False

class ZKHonestProver:
    def __init__(self, a, dim, q):
        self.a = a
        self.a_j = None
        self.n = None
        self.h = None
        self.F_q = None
        self.q = q
        self.dim = dim
        self.perm = None
        self.degree = None
        self.d_inv = None
        self.grid = None

    def perm_F_q(self):
        self.perm = np.random.permutation(np.arange(self.q))
        return self.perm

    def observe(self, a_j, n, h, F_q):
        self.a_j = a_j
        self.n = n
        self.h = h
        self.F_q = F_q
        self.degree = self.dim * (h - 1)
        self.d_inv, self.grid = precomp_denominators(self.h, self.F_q)

    def compute_g(self, mu, r, p):
        g = m_compute_g(self.a, self.a_j, mu, r, self.n, self.h, self.F_q, self.dim)
        # return : coefficients polynomial g, where g(0) = x_j and g(mu) = r
        g_0, commit, deg_g = algebraic_commitment(g, self.F_q, p)
        return g_0, commit, deg_g
    
    # prover
    def algebraic_decommitment(self, y, k):
        unlocked_evals = y[:,k]
        return unlocked_evals
    
class ZKDishonestProver(ZKHonestProver):
    def compute_g(self, mu, r, p):
        g = m_compute_g(self.a, self.a_j, mu, r, self.n, self.h, self.F_q, self.dim)
        g[0] += self.F_q(1)
        # return : coefficients polynomial g, where g(0) = x_j and g(mu) = r
        g_0, commit, deg_g = algebraic_commitment(g, self.F_q, p)
        return g_0, commit, deg_g