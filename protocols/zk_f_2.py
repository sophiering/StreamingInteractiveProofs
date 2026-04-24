#zk 2nd frequency moment 

#temporal commitment

import numpy as np

def temporal_stream(F_p):
    t_stream = np.random.permutation(F_p)
    return t_stream
# then make t_stream a stream

def temporal_commitment(filename, r):
    with open(filename, 'r') as input_stream:
        index = 0
        for val in input_stream:
            if val == r: 
                return (val, index)
            index += 1
# val will be a tuple depending on the dimensions (in our case 2D)

def check_temporal(t_stream, verifier_commit):
    value = t_stream[verifier_commit[1]]
    if value == verifier_commit[0]:
        return True
    else:
        return False

