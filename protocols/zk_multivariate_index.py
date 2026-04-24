# ZK multivariate index: extend to 3D (trivariate) vs 2D (bivariate)

# input: the length of the stream a, the stream a, the index j
# output: the jth element of a
import math
import random
import galois as g
from protocols.equality import pick_prime

# larger k = more accuracy
k = 45

a = [1,2,3,4,1,2,3,8]
j = 3

# for trivariate:
# a_j = tuple x_j (a,b,c)
# r = tuple r (d,e,f)

# prover 
def create_stream(filename, a, j):
    # creates a file containing len(a), a and j
    with open(filename, "w") as f:
        f.write(len(a) + "\n")
        for i in a:
            f.write(i + "\n")
        f.write(j + "\n")
    return filename
    
# verifier
def verifier(filename):
    # input is the length of stream a, the stream a and the index j
    with open(filename, 'r') as input_stream:
        # n: length of the input without annotation
        n = int(input_stream.readline().strip()) 
        m = n + random.randint(1,100000)
        qmin = max(pow(m, k), 3*k*h)
        # q: random prime 
        q = pick_prime(qmin)
        h = math.ceil(math.cbrt(n))
        # F_q: field for the low degree extension
        F_q = g.GF(q)
        # r: random point r (r_i,r_j) that the line will pass through alongside j
        r = [F_q(random.randint(0,q-1)), F_q(random.randint(0,q-1))]

        # precompute stage
        # precompute x
        precomp_x = F_q.Ones(h)
        for a in range(h):
            for i in range(h):
                if i != a:
                    precomp_x[a] *= (r[0] - F_q(i)) / (F_q(a) - F_q(i))
        # precompute y
        precomp_y = F_q.Ones(h)
        for a in range(h):
            for i in range(h):
                if i != a:
                    precomp_y[a] *= (r[1] - F_q(i)) / (F_q(a) - F_q(i))
        # precompute z
        precomp_z = F_q.Ones(h)
        for a in range(h):
            for i in range(h):
                if i != a:
                    precomp_z[a] *= (r[2] - F_q(i)) / (F_q(a) - F_q(i))


        # create sketch for r
        sketch = F_q(0)
        for i in range(n):
            a_i = int(next(input_stream).strip())
            # map linear index to 2D coordinates (s_a, s_b)
            s_a = i // (h * h)
            s_b = (i % (h * h)) // h
            s_c = i % h
            sketch += a_i * precomp_x[s_a] * precomp_y[s_b] * precomp_z[s_c]

    # index of 
    a_j = next(input_stream).strip()

    # check with prover
    return (a_j, r, h, F_q)

# compute g
def line_vals(a_j, t, mu, r):
    l_x = a_j[0] + (t / mu) * (r[0] - a_j[0])
    l_y = a_j[1] + (t / mu) * (r[1] - a_j[1])
    return (l_x, l_y)

# compute g
def compute_basis(h, F_q, target):
    basis = [F_q(1) * h]
    for j in range (h):
        for i in range(h):
            if i != j:
                basis[j] *= (target - F_q(i)) / (F_q(j) - F_q(i))
    return basis

# prover
def compute_g(a, n, F_q):
    # input : stream a, n, F_q
    h = math.ceil(math.sqrt(n))
    degree = 2 * h - 2
    for t in range(degree + 1):
        t_f = F_q(t)
        x, y = line_vals(t_f)
        row_basis = compute_basis(h, F_q, x)
        col_basis = compute_basis(h, F_q, y)
        
        g_vals = []
        #compute P(x,y)
        t_val = F_q(0)
        for i in range(n):
            s_a = i // h
            s_b = i % h
            t_val += F_q(a[i]) * row_basis[s_a] * col_basis[s_b]
        g_vals.append(t_val)
    return g_vals
    # return : coefficients polynomial g, where g(0) = x_j and g(mu) = r

# check g 
def interpolate_p(g, target, F_q):
    result = F_q(0)
    d = len(g) - 1
    for t in range(d + 1):
        basis_val = F_q(1)
        for i in range(d + 1):
            if i != t:
                basis_val *= (target - F_q(i)) / (F_q(t) - F_q(i))
        result += g[t] * basis_val
    return result

# verifier 
def check_g(r, g, mu, F_q):
    g_mu = interpolate_p(g, mu, F_q)
    # if initial sketch for r == g sketch for r
    if g_mu == r:
    # compute g(0)
        a_j_val = interpolate_p(g, 0, F_q)
        return a_j_val
    # else throw error
    else:
        return False
    
# prover 
def non_zk_index_protocol(input1, a, j):
    # create the stream
    create_stream(input1, a, j)

    #verifer creates its sketch
    a_j, r, n, F_q = verifier(input1)

    # prover calculates the g vals
    g = compute_g(a, n, F_q)

    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g(r, g, mu, F_q)






