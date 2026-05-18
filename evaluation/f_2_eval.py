import math 
import numpy as np 
import galois as g
import time
import sys
import gc
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from stream_generation.gen_freq_moments import f_2_eval
from protocols.freq_moments import sketch_2d, h_2d_t, h_2d_f, verify
from protocols.f_2_multivariate import m_create_sketch, HonestProver, DishonestProver, verify_round, final_check

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
        for i in range(10):
            v, t = f_2_t_eval(filename, helpername, n)
            honest_verdicts.append(v)
            honest_times.append(t)
        # dishonest prover tests
        for i in range(10):
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

def eval_f_2_m(filename, n_vals, dim):
    honest_correctness =[]
    dishonest_correctness = []
    honest_runtimes = []
    dishonest_runtimes = []
    honest_min = []
    dishonest_min = []
    honest_max = []
    dishonest_max = []
    f_2_t_m(filename, 100, dim)
    for n in n_vals:
        honest_verdicts = []
        dishonest_verdicts = []
        honest_times = []
        dishonest_times = []
        # honest prover tests
        for i in range(10):
            v, t = f_2_t_m(filename, n, dim)
            honest_verdicts.append(v)
            honest_times.append(t)
        # dishonest prover tests
        for i in range(10):
            v, t = f_2_f_m(filename, n, dim)
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

def f_2_t_m(filename, n, dim):
    f_2_eval(filename,n)
    gc.collect()
    start_time = time.perf_counter()
    F_q, r_challenges, h, f_eval = m_create_sketch("f_2_3d.txt", dim)
    prover = HonestProver("f_2_3d.txt", dim, F_q)
    expected_sum = None
    claimed_f_2 = None
    # k rounds of sum check
    for k in range(dim):
        P_k = prover.gen_polynomial()
        result = verify_round(P_k, F_q, r_challenges[k], h, expected_sum)
        if result == False:
            return False
        expected_sum, actual_sum = result
        if k == 0:
            claimed_f_2 = actual_sum
        prover.reply(r_challenges[k])
    f2_result = final_check(expected_sum, f_eval, claimed_f_2)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    if f2_result == prover.grid:
        # verify did not fail
        result = 0
    else:
        result = 1
    return (result, run_time)

def f_2_f_m(filename, n, dim):
    f_2_eval(filename,n)
    gc.collect()
    start_time = time.perf_counter()
    F_q, r_challenges, h, f_eval = m_create_sketch("f_2_3d.txt", dim)
    prover = DishonestProver("f_2_3d.txt", dim, F_q)
    expected_sum = None
    claimed_f_2 = None
    f2_result = True
    # k rounds of sum check
    for k in range(dim):
        P_k = prover.gen_polynomial(F_q)
        result = verify_round(P_k, F_q, r_challenges[k], h, expected_sum)
        if result == False:
            f2_result = False
            break
        expected_sum, actual_sum = result
        if k == 0:
            claimed_f_2 = actual_sum
        prover.reply(r_challenges[k])
    if f2_result:
        f2_result = final_check(expected_sum, f_eval, claimed_f_2)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    if f2_result == False:
        # verify did not fail
        result = 0
    else:
        result = 1
    return (result, run_time)