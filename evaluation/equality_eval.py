import math 
import random
import numpy as np 
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from protocols.equality import equality_check
from stream_generation.gen_equality import true_eq, false_eq

def eval_eq(filename):
    n_vals = [int(math.pow(2,10)), int(math.pow(2,15)), int(math.pow(2,20))]
    eq_correctness = []
    neq_correctness = []
    eq_runtimes = []
    neq_runtimes = []
    for n in n_vals:
#        for i in range(10):
        eq_verdicts = []
        neq_verdicts = []
        eq_times = []
        neq_times = []
        for i in range(9):
            true_eq(filename)
            v, t = equality_check(filename)
            eq_verdicts.append(v)
            eq_times.append(t)
        for i in range(9):
            false_eq(filename)
            v, t = equality_check(filename)
            neq_verdicts.append(v)
            neq_times.append(t)
        # why are we getting RuntimeWarning: Mean of empty slice. RuntimeWarning: invalid value encountered in scalar divide ret = ret.dtype.type(ret / rcount) errors after 10?
        print(eq_verdicts)
        print(neq_verdicts)
        eq_correctness.append(np.count_nonzero(eq_verdicts) / len(eq_verdicts) * 100)
        neq_correctness.append((len(neq_verdicts) - np.count_nonzero(neq_verdicts)) / len(neq_verdicts) * 100)
        eq_runtimes.append(np.mean(eq_times))
        neq_runtimes.append(np.mean(neq_times))
    return eq_correctness, eq_runtimes, neq_correctness, neq_runtimes

