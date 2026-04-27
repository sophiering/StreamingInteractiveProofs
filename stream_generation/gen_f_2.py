import random
import numpy as np
import math

def frequencies(filename):
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    with open(filename, "w") as f:
        f.write(f"{n}\n")
    with open(filename, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
    return n, s

def h_2d(n, s, q):
    F_q = g.GF(q)
    h = math.ceil(math.sqrt(n))
    d = (2 * h) - 1
    s_prime = F_q.zeros(d)
    # precompute weights for the Lagrange polynomial reconstruction
    precompute = []
    for X in range(d):
        X_fq = F_q(X)
        basis = F_q.Ones(h)
        for a in range(h):
            for i in range(h):
                if i != a:
                    basis[a] *= (X_fq - F_q(i)) / (F_q(a) - F_q(i))
        precompute.append(basis)

    # use precomputed weights to compute f
    # over columns (y)
    for y in range(h):
        for X in range(d):
            # start calculating f_tilde(X,y)
            f_tilde = F_q(0)
            # over rows (x)
            for i in range(h):
                index = i * h + y
                if index < n:
                    s_val = s[index]
                else:
                    s_val = F_q(0)
                f_tilde += precompute[X][i] * s_val
                s_prime[X] += f_tilde ** 2
    return s_prime




def f2_3d():
    pass