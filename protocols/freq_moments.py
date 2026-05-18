# frequency moments: F_2
# input: length of stream a, the stream a, the helper's annotation
# output: the frequency moment 
import math
import time
import numpy as np
import galois as g
import secrets
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.equality import pick_prime, stream_generator
from stream_generation.gen_freq_moments import f_s, f_2_s

# larger k = more accuracy
k = 45

# 0th frequency moment
def f_0(filename):
    # prover creates stream
    f_s(filename)
    # verifier counts items
    f_0 = f_0_v(filename)
    return f_0

def f_0_v(filename):
    f_0 = 0
    filepath = base_path / "streams" / filename
    stream = stream_generator(filepath)
    with open(filepath, 'r') as stream:
        for item in stream:
            f_0 += 1
    return f_0

# 1st frequency moment
def f_1(filename):
    # prover creates stream
    # f_s(filename)
    # verifier counts items
    f_1 = f_1_v(filename)
    return f_1

def f_1_v(filename):
    f_1 = 0
    filepath = base_path / "streams" / filename
    stream = stream_generator(filepath)
    with open(filepath, "r") as stream:
        for item in stream:
            f_1 += int(item)
    return f_1

# 2nd frequency moment with correct helper annotation (should correctly calculate F_2)
def f_2_t(filename, helpername):
    # create frequency stream
    # n, s = f_2_s(filename)
    # generate sketch
    q, r, h, v_sketch = sketch_2d(filename, k)
    # create helper annotation
    h_2d_t(helpername, n, s, q)
    # verify
    f_2 = verify(v_sketch, helpername, g.GF(q), r, h)
    return f_2


# 2nd frequency moment with bad helper annotation (should fail)
def f_2_f(filename, helpername):
    # create frequency stream
    # n, s = f_2_s(filename)
    # generate sketch
    q, r, h, v_sketch = sketch_2d(filename, k)
    # create bad helper annotation
    h_2d_f(helpername, n, s, q) 
    # verify should return -1
    f_2 = verify(v_sketch, helpername, g.GF(q), r, h)
    return f_2

def sketch_2d(filename, k):
    filepath = base_path / "streams" / filename
    # input is the elements followed by the helper's annotation: a_1, ... a_n, s'(x)
    stream = stream_generator(filepath)
    # length of the input without annotation
    n = next(stream) 
    h = math.ceil(math.sqrt(n))
    q = 2147483647
    F_q = g.GF(q)
    r = F_q(secrets.randbelow(q))
    # precompute stage
    # precompute rows
    numerator_rows = F_q(1)
    for i in range(h):
        numerator_rows *= (r - F_q(i))
    precomp_rows = F_q.Ones(h)
    for a in range(h):
        denominator_rows = math.factorial(a) * ((-1) ** (h-1-a)) * math.factorial(h-1-a)
        denominator_rows = F_q(denominator_rows % q)
        precomp_rows[a] = numerator_rows / ((r - F_q(a)) * denominator_rows)
    # piece together sketch
    sketch = F_q.Zeros(h)       
    for item in range(n):
        value = next(stream)
        current_value = F_q(value)
        # map to 2D coordinates (s_a, s_b)
        s_a = item // h
        s_b = item % h
        # build f(r,i) values for i in [1,n]
        sketch[s_b] += precomp_rows[s_a] * current_value
    return q, r, h, sketch

# honest prover
def h_2d_t(helpername, n, s, q):
    filepath = base_path / "streams" / helpername
    F_q = g.GF(q)
    h = math.ceil(math.sqrt(n))
    d = (2 * h) - 1
    # precompute weights 
    precompute = F_q.Zeros((d,h), dtype=np.int64)
    denominators = F_q.Ones(h)
    for a in range(h):
        for i in range(h):
            if i != a:
                denominators[a] *= (F_q(a) - F_q(i))
    for X in range(d):
        X_fq = F_q(X)
        if 0 <= X < h:
            precompute[X,X] = F_q(1)
        else:
            common_num = F_q(1)
            for i in range(h):
                common_num *= (X_fq - F_q(i))
            for a in range(h):
                precompute[X,a] = common_num / ((X_fq - F_q(a)) * denominators[a])
    # use precomputed weights to compute f over columns (y)
    s_padded = np.zeros(h*h, dtype=np.int64)
    s_len = min(n, len(s))
    s_padded[:s_len] = s[:s_len]
    grid = F_q(s_padded).reshape((h,h))
    # computes all elements at once vs element by element
    f_tilde = np.matmul(precompute, grid)
    # turn h x h matrix into 1 x h array
    s_prime = np.sum(f_tilde ** 2, axis=1)
    with open(filepath, "w") as f:
        for element in s_prime:
            f.write(f"{int(element)}\n")
    return s_prime

# dishonest prover
def h_2d_f(helpername, n, s, q):
    filepath = base_path / "streams" / helpername
    F_q = g.GF(q)
    h = math.ceil(math.sqrt(n))
    d = (2 * h) - 1
    # precompute weights 
    precompute = F_q.Zeros((d,h))
    denominators = F_q.Ones(h)
    for a in range(h):
        for i in range(h):
            if i != a:
                denominators[a] *= (F_q(a) - F_q(i))
    for X in range(d):
        X_fq = F_q(X)
        if 0 <= X < h:
            precompute[X,X] = F_q(1)
        else:
            common_num = F_q(1)
            for i in range(h):
                common_num *= (X_fq - F_q(i))
            for a in range(h):
                precompute[X,a] = common_num / ((X_fq - F_q(a)) * denominators[a])
    # use precomputed weights to compute f over columns (y)
    s_padded = np.zeros(h*h, dtype=np.int64)
    s_len = min(n, len(s))
    for x in s[:s_len]:
        s_padded[:s_len] = int(x) 
    grid = F_q(s_padded).reshape((h,h))
    # computes all elements at once vs element by element
    f_tilde = np.matmul(precompute, grid)
    # turn h x h matrix into 1 x h array
    s_prime = np.sum(f_tilde ** 2, axis=1)
    # alter s'(X) to simulate malicious helper annotation
    s_prime[0] += F_q(1)
    with open(filepath, "w") as f:
        for element in s_prime:
            f.write(f"{int(element)}\n")
    return s_prime

# sumcheck
def verify(sketch, h_annotation, F_q, r, h):
    filepath = base_path / "streams" / h_annotation
    # input is the elements followed by the helper's annotation: a_1, ... a_n, s'(x)
    stream = stream_generator(filepath)
    # length of the input without annotation
    d = (2 * int(h)) - 1
    r = F_q(r)
    # calculate sketch s(r)
    total1 = F_q(0)
    for s_val in sketch:
        total1 += s_val ** 2
    # precompute to aid s'(r) computation
    common_numerator = F_q(1)
    for i in range(d):
        common_numerator *= (r - F_q(i))
    denominators = F_q.Ones(d) 
    for X in range(d):
        for i in range(d):
            if i != X:
                denominators[X] *= (F_q(X) - F_q(i))
    total2 = F_q(0)      
    f_2 = F_q(0) 
    # form s'(r)
    with open(filepath, "r") as stream:
        for X in range(d):
            s_val = F_q(int(next(stream)))
            # increment f_2 in case helper annotation is deemed trustworthy 
            if X < h:
                f_2 += s_val
            if r == F_q(X):
                total2 = s_val
            else:
                l_x_r = common_numerator / ((r - F_q(X)) * denominators[X])
                total2 += s_val * l_x_r
    # complete check to see if helper annotation can be trusted: s'(r) = s(r)
    if total1 == total2:
        return int(f_2)
    else:
        return False
