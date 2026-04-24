# ZK index

# input: the length of the stream a, the stream a, the index j
# output: the jth element of a
import math
import random
import secrets
import galois as g
from protocols.non_zk_index import create_stream, verifier, compute_g, check_g, interpolate_p

# we start with a consisting of a_1 to a_n
# we create the l(x,r) line 
# for non zk we would just send f evaluated at all the points f_{a_1}, ... f_{a_n} 

def pad_value(value, F_q):
    pad_left = F_q(secrets.randbelow(F_q.order))
    pad_right = F_q(secrets.randbelow(F_q.order))
    padded = pad_left + value + pad_right + len(pad_left)
    return padded
    
# verifier 
def check_g_zk(sketch, zk_vals, mu, F_q):
    unpadded_zk_vals = []
    for i in zk_vals:
        F_q, mu, r, sketch, n, h, a_j = verifier(i)
        g = compute_g(a, a_j, mu, r, n, h, F_q)
        unpadded_zk_vals.append(check_g(sketch, g, mu, F_q))
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
    # create the stream
    create_stream(input1, a, j)

    #verifer creates its sketch
    F_q, mu, r, sketch, n, h, a_j = verifier(input1)

    # prover calculates the g vals
    g_vals = compute_g(a, a_j, mu, r, n, h, F_q)

    zk_vals = []
    for i in g_vals:
        padded = pad_value(i, F_q)
        zk_vals.append(padded)

    #verifier interpolates the values provided by the prover, checks it agrees with prover and returns a_j if so
    return check_g_zk(sketch, zk_vals, mu, F_q)





