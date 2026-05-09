import random
import numpy as np
import math
import galois as g

from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

def f_s(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    with open(filepath, "w") as f:
        np.savetxt(f, s, fmt = '%d')
    # n is used to verify 
    return n

def f_1_test(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    f_1 = np.sum(s)
    with open(filepath, "w") as f:
        np.savetxt(f, s, fmt = '%d')
    # n is used to verify 
    return f_1

def f_2_s(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
    return n, s

def f_2_h_2d_t(helpername, n, s, q):
    filepath = base_path / "streams" / helpername
    F_q = g.GF(q)
    h = math.ceil(math.sqrt(n))
    d = (2 * h) - 1
    s_prime = F_q.Zeros(d)
    # precompute weights for the Lagrange polynomial reconstruction
    denominators = F_q.Ones(h)
    for a in range(h):
        for i in range(h):
            if i != a:
                denominators[a] *= (F_q(a) - F_q(i))
    precompute = []
    for X in range(d):
        X_fq = F_q(X)
        basis = F_q.Zeros(h)
        if 0 <= X < h:
            basis[int(X)] = F_q(1)
        else:
            common_num = F_q(1)
            for i in range(h):
                common_num *= (X_fq - F_q(i))
            for a in range(h):
                basis[a] = common_num / ((X_fq - F_q(a)) * denominators[a])
        precompute.append(basis)
    # use precomputed weights to compute f over columns (y)
    for y in range(h):
        # calculate the column values f_tilde(0, y), f_tilde(1, y) ... f_tilde(h-1, y)
        column_values = F_q([s[i * h + y] if (i * h + y) < n else 0 for i in range(h)])
        for X in range(d):
            # compute the evaluation of the row polynomial at point X f_tilde(X, y) 
            f_tilde = np.dot(precompute[X], column_values)
            # increment s'(X)
            s_prime[X] += f_tilde ** 2
    with open(filepath, "w") as f:
        for element in s_prime:
            f.write(f"{int(element)}\n")
    return s_prime

def f_2_h_2d_f(helpername, n, s, q):
    filepath = base_path / "streams" / helpername
    F_q = g.GF(q)
    h = math.ceil(math.sqrt(n))
    d = (2 * h) - 1
    s_prime = F_q.Zeros(d)
    # precompute weights for the Lagrange polynomial reconstruction
    denominators = F_q.Ones(h)
    for a in range(h):
        for i in range(h):
            if i != a:
                denominators[a] *= (F_q(a) - F_q(i))
    precompute = []
    for X in range(d):
        X_fq = F_q(X)
        basis = F_q.Zeros(h)
        if 0 <= X < h:
            basis[int(X)] = F_q(1)
        else:
            common_num = F_q(1)
            for i in range(h):
                common_num *= (X_fq - F_q(i))
            for a in range(h):
                basis[a] = common_num / ((X_fq - F_q(a)) * denominators[a])
        precompute.append(basis)
    # use precomputed weights to compute f over columns (y)
    for y in range(h):
        # calculate the column values f_tilde(0, y), f_tilde(1, y) ... f_tilde(h-1, y)
        column_values = F_q([s[i * h + y] if (i * h + y) < n else 0 for i in range(h)])
        for X in range(d):
            # compute the evaluation of the row polynomial at point X f_tilde(X, y) 
            f_tilde = np.dot(precompute[X], column_values)
            # increment s'(X)
            s_prime[X] += f_tilde ** 2
    # alter s'(X) to simulate malicious helper annotation
    s_prime[0] += F_q(1)
    with open(filepath, "w") as f:
        for element in s_prime:
            f.write(f"{int(element)}\n")
    return s_prime

def f_2_h_3d():
    pass