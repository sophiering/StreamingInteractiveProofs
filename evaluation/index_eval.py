import math 
import numpy as np 
import time
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.index import verifier, compute_g, check_g
from protocols.index_multivariate import m_verifier, m_compute_g, m_check_g
from stream_generation.gen_index import index_eval

def eval_index(filename, n_vals):
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
            v, t = index_t_eval(filename, n)
            honest_verdicts.append(v)
            honest_times.append(t)
        # dishonest prover tests
        for i in range(10):
            v, t = index_f_eval(filename, n)
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

def index_t_eval(filename, n):
    start_time = time.perf_counter()
    a, true_a_j = index_eval(filename,n)
    F_q, mu, r, sketch, n, h, a_j = verifier(filename)
    g = compute_g(a, a_j, mu, r, n, h, F_q)
    if check_g(sketch, g, mu, F_q) == true_a_j:
        # correctly finds a_j
        result = 1
    else:
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def index_f_eval(filename, n):
    start_time = time.perf_counter()
    a, _ = index_eval(filename,n)
    F_q, mu, r, sketch, n, h, a_j = verifier(filename)
    g = compute_g(a, a_j, mu, r, n, h, F_q)
    g = np.random.permutation(g)
    if check_g(sketch, g, mu, F_q) == False:
        # correctly terminated
        result = 1
    else:
        # did not terminate
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def eval_multivariate(filename, n_vals, dim):
    honest_correctness =[]
    dishonest_correctness = []
    honest_runtimes = []
    dishonest_runtimes = []
    honest_min = []
    dishonest_min = []
    honest_max = []
    dishonest_max = []
    # for dim in range(2,4):
    for n in n_vals:
        honest_verdicts = []
        dishonest_verdicts = []
        honest_times = []
        dishonest_times = []
        # honest prover tests
        for i in range(10):
            v, t = multivariate_t_eval(filename, dim, n)
            honest_verdicts.append(v)
            honest_times.append(t)
        # dishonest prover tests
        for i in range(10):
            v, t = multivariate_f_eval(filename, dim, n)
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

def multivariate_t_eval(filename, dim, n):
    start_time = time.perf_counter()
    a, true_a_j = index_eval(filename,n)
    F_q, mu, r, sketch, n, h, a_j = m_verifier(filename, dim)
    g = m_compute_g(a, a_j, mu, r, n, h, F_q, dim)
    if m_check_g(sketch, g, mu, F_q) == true_a_j:
        # correctly finds a_j
        result = 1
    else:
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def multivariate_f_eval(filename, dim, n):
    start_time = time.perf_counter()
    a, _ = index_eval(filename,n)
    F_q, mu, r, sketch, n, h, a_j = m_verifier(filename, dim)
    g = m_compute_g(a, a_j, mu, r, n, h, F_q, dim)
    g = np.random.permutation(g)
    if m_check_g(sketch, g, mu, F_q) == False:
        # correctly terminated
        result = 1
    else:
        # did not terminate
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)
