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


from protocols.equality import pick_prime, stream_generator
from stream_generation.gen_freq_moments import f_2_s, f_2_h_2d_t, f_2_h_2d_f

# larger k = more accuracy
k = 45



# 2nd frequency moment with correct helper annotation (should correctly calculate F_2)
def f_2_t(filename, helpername, k, dim):
    # create frequency stream
    n, s = f_2_s(filename)
    # generate sketch
    q, r, h, v_sketch = create_sketch(filename, k, dim)
    # create helper annotation
    f_2_h_2d_t(helpername, n, s, q, dim)
    # verify
    f_2 = verify(v_sketch, helpername, g.GF(q), r, h, dim)
    return f_2


# 2nd frequency moment with bad helper annotation (should fail)
def f_2_f(filename, helpername, k):
    # create frequency stream
    n, s = f_2_s(filename)
    # generate sketch
    q, r, h, v_sketch = create_sketch(filename, k)
    # create bad helper annotation
    f_2_h_2d_f(helpername, n, s, q) 
    # verify should return -1
    f_2 = verify(v_sketch, helpername, g.GF(q), q, r, h)
    return f_2

def create_sketch(filename, k, dim):
    filepath = base_path / "streams" / filename
    # input is the elements followed by the helper's annotation: a_1, ... a_n, s'(x)
    stream = stream_generator(filepath)
    # length of the input without annotation
    n = next(stream) 
    m = n + random.randint(1,100000)
    h = math.ceil(math.pow(n, 1/dim))
    shape = [h] * dim
    qmin = max(math.pow(m,k), 3*k*h)
    q = pick_prime(qmin, k)
    q_chosen = False
    while q_chosen == False:
        # field for the low degree extension
        try:
            F_q = g.GF(q)
            q_chosen = True
        except ValueError:
            q = pick_prime(qmin, k)
    r = [F_q(secrets.randbelow(q))] * dim
    # precompute 
    precomp = np.ones((dim,h))
    for dimension in dim:
        for a in range(h):
            for i in range(h):
                if i != a:
                    precomp[dimension][a] *= (r[dimension] - F_q(i)) / (F_q(a) - F_q(i))      
    # create the h x v matrix
    sketch = F_q.Zeros(h)    
    for item in range(n):
        # map to 3D coordinates (s_a, s_b, s_c)
        value = next(stream)
        current_value = F_q(value)
        k_dim_v = np.unravel_index(item, shape)
        total = 1
        for dimension in range(dim):
            total *= precomp[dimension][k_dim_v[dimension]]
        sketch[k_dim_v[-1]] += current_value * total
    return q, r, h, sketch

# sumcheck
def verify(sketch, h_annotation, F_q, r, h, dim):
    filepath = base_path / "streams" / h_annotation
    # input is the elements followed by the helper's annotation: a_1, ... a_n, s'(x)
    stream = stream_generator(filepath)
    # length of the input without annotation
    d = (2 * h) - 1
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
        print("True")
        return int(f_2)
    else:
        print("False")
        return -1