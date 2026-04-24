# non ZK index 

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

# for bivariate:
# a_j = tuple x_j (a,b)
# r = tuple r (c,d)

# works!
# prover 
def create_stream(filename, a, j):
    # creates a file containing len(a), a and j
    with open(filename, "w") as f:
        f.write(str(len(a)) + "\n")
        for i in a:
            f.write(str(i) + "\n")
        f.write(str(j) + "\n")
    return filename
    
# verifier
def verifier(filename):
    # input is the length of stream a, the stream a and the index j
    with open(filename, 'r') as input_stream:
        k = 45
        # n: length of the input without annotation
        n = int(input_stream.readline().strip()) 
        h = math.ceil(math.sqrt(n))
        m = n + random.randint(1,100000)
        qmin = max(pow(m, k), 3*k*h)
        # q: random prime 
        q = pick_prime(qmin,k)
        # F_q: field for the low degree extension
        F_q = g.GF(q)
        # mu: non-zero element of F_q
        mu = F_q(random.randint(1,q-1))
        # r: random point r (r_i,r_j) that the line will pass through alongside j
        r = [F_q(random.randint(0,q-1)), F_q(random.randint(0,q-1))]

        # precompute stage
        # precompute rows
        precomp_rows = F_q.Ones(h)
        for a in range(h):
            for i in range(h):
                if i != a:
                    precomp_rows[a] *= (r[0] - F_q(i)) / (F_q(a) - F_q(i))
        # precompute columns
        precomp_cols = F_q.Ones(h)
        for a in range(h):
            for i in range(h):
                if i != a:
                    precomp_cols[a] *= (r[1] - F_q(i)) / (F_q(a) - F_q(i))

        # create sketch for r
        sketch = F_q(0)
        for i in range(n):
            a_i = int(next(input_stream).strip())
            # map linear index to 2D coordinates (s_a, s_b)
            s_a = i // h
            s_b = i % h
            sketch += a_i * precomp_rows[s_a] * precomp_cols[s_b]

    # index of 
    j = int(next(input_stream).strip())
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
    basis = [F_q(1)] * h
    for j in range (h):
        for i in range(h):
            if i != j:
                basis[j] *= (target - F_q(i)) / (F_q(j) - F_q(i))
    return basis

# prover
def compute_g(a, a_j, mu, r, n, h, F_q):
    degree = 2 * h - 2
    g_vals = []
    for t in range(degree + 1):
        t_f = F_q(t)
        x, y = line_vals(a_j, t_f, mu, r)
        row_basis = compute_basis(h, F_q, x)
        col_basis = compute_basis(h, F_q, y)
        grid = [a[i:i + h] for i in range(0, n, h)]
        #compute P(x,y)
        for s_a in range(h):
            row_contribution = row_basis[s_a]
            if row_contribution == 0: continue # Skip if no impact
            
            row_sum = F_q(0)
            for s_b in range(h):
                row_sum += F_q(grid[s_a][s_b]) * col_basis[s_b]
            
            t_val += row_contribution * row_sum

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
def check_g(sketch, g, mu, F_q):
    g_mu = interpolate_p(g, mu, F_q)
    # if initial sketch for r == g sketch for r
    if g_mu == sketch:
    # compute g(0)
        a_j_val = interpolate_p(g, 0, F_q)
        print(a_j_val)
        return a_j_val
    # else throw error
    else:
        print(False)
        return False
    
# prover 
def non_zk_index_protocol(input1, a, j):
    print("1")
    # create the stream
    create_stream(input1, a, j)
    print("2")
    #verifer creates its sketch
    F_q, mu, r, sketch, n, h, a_j = verifier(input1)
    print("3")
    # prover calculates the g vals
    g = compute_g(a, a_j, mu, r, n, h, F_q)
    print("4")
    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g(sketch, g, mu, F_q)






