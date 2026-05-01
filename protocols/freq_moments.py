# frequency moments: F_2
# input: length of stream a, the stream a, the helper's annotation
# output: the frequency moment 
import math
import random
import galois as g
from protocols.equality import pick_prime, stream_generator
from stream_generation.gen_freq_moments import f_1_s, f_2_s, f_2_h_2d_t, f_2_h_2d_f, f_2_h_3d

# larger k = more accuracy
k = 45

# 1st frequency moment
def f_1(filename):
    f_1_s(filename)
    f_1 = 0
    with open(filename, 'r') as stream:
        for item in stream:
            f_1 += 1
    return f_1

# 2nd frequency moment with correct helper annotation (should correctly calculate F_2)
def f_2_t(filename, k):
    # create frequency stream
    n, s = f_2_s(filename)
    # generate sketch
    q, r, h, v_sketch = create_sketch(filename, k)
    # create helper annotation
    f_2_h_2d_t(n, s, q)
    # stream in helper annotation
    h_annotation = helper(filename, q)
    # verify
    verify(v_sketch, h_annotation, g.GF(q), r, h)

# 2nd frequency moment with bad helper annotation (should fail)
def f_2_f(filename, k):
    # create frequency stream
    n, s = f_2_s(filename)
    # generate sketch
    q, r, h, v_sketch = create_sketch(filename, k)
    # TODO: create bad helper annotation
    f_2_h_2d_f(n, s, q) 
    # stream in helper annotation
    h_annotation = helper(filename, q)
    # verify
    verify(v_sketch, h_annotation, g.GF(q), r, h)

def create_sketch(filename, k):
    # input is the elements followed by the helper's annotation: a_1, ... a_n, s'(x)
    stream = stream_generator(filename)
    # length of the input without annotation
    n = next(stream) 
    m = n + random.randint(1,100000)
    h = math.ceil(math.sqrt(n))
    qmin = max(pow(m, k), 3*k*h)
    q = pick_prime(qmin)
    # field for the low degree extension
    F_q = g.GF(q)
    r = F_q(random.randint(0,q-1))
    
    # precompute 
    precompute = F_q.Ones(h)
    for a in range(h):
        for i in range(h):
            if i != a:
                precompute[a] *= (r - F_q(i)) / (F_q(a) - F_q(i))

    sketch = F_q.zeros(h)       
    # create the h x v matrix
    for item in stream:
        current = int(stream.readline().strip())
        current_value = F_q(current)
        # map to 2D coordinates (s_a, s_b)
        s_a = item // h
        s_b = item % h
        sketch[s_b] += precompute[s_a] * current_value
    return q, r, h, sketch

def helper(filename, q):
    F_q = g.GF(q)
    with open(filename, 'r') as stream:
        h_annotation = []
        for h_val in stream:
            h_annotation.append(F_q(int(h_val.strip())))
    return h_annotation

# sumcheck
def verify(sketch, h_annotation, F_q, r, h):
    h_len = len(h_annotation)
    total1 = F_q(0)
    for s_val in sketch:
        total1 += s_val ** 2
    
    total2 = F_q(0)
    # edge case (prevents divide by zero error later on)
    exact_match = False
    for i in range(h_len):
        if r == F_q(i):
            total2 = h_annotation[i]
            exact_match = True
            break
    
    if not exact_match:
        l_r = F_q(1)
        for i in range(h_len):
            l_r *= (r-F_q(i))

        barycentric_sum = F_q(0)
        for i in range(h_len):
            w_i_inv = F_q(1)
            for j in range(h_len):
                if i != j:
                    w_i_inv *= (F_q(i) - F_q(j))
            
            w_i = F_q(1) / w_i_inv  
            term = (h_annotation[i] * w_i) / (r - F_q(i))
            barycentric_sum += term
        total2 = l_r * barycentric_sum

    if total1 == total2:
        print("True")
        f_2 = F_q(0)
        for i in range(h):
            f2 += h_annotation[i]
        return f_2
    else:
        print("False")
        return -1

