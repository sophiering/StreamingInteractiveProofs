import math 
import numpy as np 
import galois as g
import time
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.freq_moments import sketch_2d, h_2d_t, h_2d_f, verify
from stream_generation.gen_freq_moments import f_2_eval

k = 24

def eval_f_2(filename, helpername, n_vals):
    honest_correctness =[]
    dishonest_correctness = []
    honest_runtimes = []
    dishonest_runtimes = []
    honest_min = []
    dishonest_min = []
    honest_max = []
    dishonest_max = []
    for n in n_vals:
        honest_verdicts = []
        dishonest_verdicts = []
        honest_times = []
        dishonest_times = []
        # honest prover tests
        for i in range(1):
            v, t = f_2_t_eval(filename, helpername, n)
            honest_verdicts.append(v)
            honest_times.append(t)
        # dishonest prover tests
        for i in range(1):
            v, t = f_2_f_eval(filename, helpername, n)
            dishonest_verdicts.append(v)
            dishonest_times.append(t)
        honest_correctness.append(np.count_nonzero(honest_verdicts) / len(honest_verdicts) * 100)
        dishonest_correctness.append(np.count_nonzero(dishonest_verdicts) / len(dishonest_verdicts) * 100)
        honest_runtimes.append(np.mean(honest_times))
        dishonest_runtimes.append(np.mean(dishonest_times))
        honest_min.append(np.min(honest_times))
        dishonest_min.append(np.min(dishonest_times))
        honest_max.append(np.max(honest_times))
        dishonest_max.append(np.max(dishonest_times))
    return honest_correctness, honest_runtimes, honest_min, honest_max, dishonest_correctness, dishonest_runtimes, dishonest_min, dishonest_max

def f_2_t_eval(filename, helpername, n):
    start_time = time.perf_counter()
    s = f_2_eval(filename,n)
    q, r, h, v_sketch = sketch_2d(filename, k)
    h_2d_t(helpername, n, s, q)
    if verify(v_sketch, helpername, g.GF(q), r, h) == False:
        # verify did not fail
        result = 0
    else:
        result = 1
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def f_2_f_eval(filename, helpername, n):
    start_time = time.perf_counter()
    start_time = time.perf_counter()
    s = f_2_eval(filename,n)
    q, r, h, v_sketch = sketch_2d(filename, k)
    h_2d_f(helpername, n, s, q)
    if verify(v_sketch, helpername, g.GF(q), r, h) == False:
        # correctly terminated
        result = 1
    else:
        # did not terminate
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

