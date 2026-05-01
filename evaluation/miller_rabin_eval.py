import math 
import random
import numpy as np 
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from protocols.equality import prime_check

def eval_mr():
    q_primes = [2, 31, 7237, 7879, 29851, 29959, 42083, 396997, 405749, 108967]
    q_composites = [561, 6601, 1729, 2821, 17039, 42309, 43713, 81407, 108963, 2047, 11305, 2981, 41041, 9881, 7657, 8023, 8029, 8401, 8911, 9881]
    k_vals = [1,2,3,4,5,10,15,30,45]
    prime_correctness = []
    composite_correctness = []
    prime_runtimes = []
    composite_runtimes = []
    for k in k_vals:
        q_verdicts = []
        c_verdicts = []
        q_runtimes = []
        c_runtimes = []
        for q in q_primes:
            verdict, runtime = prime_check(q, k)
            q_verdicts.append(verdict)
            q_runtimes.append(runtime)
        for c in q_composites:
            verdict, runtime = prime_check(c, k)
            c_verdicts.append(verdict)
            c_runtimes.append(runtime)
        q_correctness = np.count_nonzero(q_verdicts) / len(q_verdicts) * 100
        c_correctness = (len(c_verdicts) - np.count_nonzero(c_verdicts)) / len(c_verdicts) * 100
        prime_correctness.append(q_correctness)
        composite_correctness.append(c_correctness)
        prime_runtimes.append(np.mean(q_runtimes))
        composite_runtimes.append(np.mean(c_runtimes))
    return prime_correctness, prime_runtimes, composite_correctness, composite_runtimes
