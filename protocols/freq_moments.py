# frequency moments: F_2
# input: length of stream a, the stream a, the helper's annotation
# output: the frequency moment 
import math
import random
import galois as g
from protocols.equality import pick_prime

# larger k = more accuracy
k = 45

def create_sketch(filename, k):
    # input is the elements followed by the helper's annotation: a_1, ... a_n, s'(x)
    with open(filename, 'r') as stream:
        # length of the input without annotation
        n = int(stream.readline().strip()) 
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
        for item in range(n):
            current = int(stream.readline().strip())
            current_value = F_q(current)
            # map to 2D coordinates (s_a, s_b)
            s_a = item // h
            s_b = item % h
            sketch[s_b] += precompute[s_a] * current_value

        h_annotation = []
        for h_val in stream:
            h_annotation.append(F_q(int(h_val.strip())))

# sumcheck
def verify(sketch, h_annotation, F_q, r, h):
    total1 = F_q(0)
    for s_val in sketch:
        total1 += s_val ** 2
    
    total2 = F_q(0)
    for h_val in reversed(h_annotation):
        total2 = (total2 * r) + h_val

    if total1 == total2:
        print("True")
        # we want to calculate F_2 here
        f2 = F_q(0)
        for x_val in range(h):
                field_x = F

        return f2
    else:
        print("False")
        return -1