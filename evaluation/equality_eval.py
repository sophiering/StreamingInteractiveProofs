import math 
import numpy as np 
import time
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.equality import equality_check, eq_fixed_q
from stream_generation.gen_equality import true_eval, false_eval

def eval_eq(filename, n_vals):
    eq_correctness = []
    neq_correctness = []
    eq_runtimes = []
    neq_runtimes = []
    eq_min = []
    neq_min = []
    eq_max = []
    neq_max = []
    for n in n_vals:
        eq_verdicts = []
        neq_verdicts = []
        eq_times = []
        neq_times = []
        for i in range(10):
            v, t = true_eq(filename, n)
            eq_verdicts.append(v)
            eq_times.append(t)
        for i in range(10):
            v,t = false_eq(filename, n)
            neq_verdicts.append(v)
            neq_times.append(t)
        eq_correctness.append(np.count_nonzero(eq_verdicts) / len(eq_verdicts) * 100)
        neq_correctness.append((len(neq_verdicts) - np.count_nonzero(neq_verdicts)) / len(neq_verdicts) * 100)
        eq_runtimes.append(np.mean(eq_times))
        neq_runtimes.append(np.mean(neq_times))
        eq_min.append(np.min(eq_times))
        neq_min.append(np.min(neq_times))
        eq_max.append(np.max(eq_times))
        neq_max.append(np.max(neq_times))
    return eq_correctness, eq_runtimes, eq_min, eq_max, neq_correctness, neq_runtimes, neq_min, neq_max

def true_eq(filename, n):
    start_time = time.perf_counter()
    true_eval(filename, n)
    result = equality_check(filename)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def false_eq(filename, n):
    start_time = time.perf_counter()
    false_eval(filename, n)
    result = equality_check(filename)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def exc_mr(filename, n_vals):
    eq_correctness = []
    neq_correctness = []
    eq_runtimes = []
    neq_runtimes = []
    eq_min = []
    neq_min = []
    eq_max = []
    neq_max = []
    for n in n_vals:
        eq_verdicts = []
        neq_verdicts = []
        eq_times = []
        neq_times = []
        for i in range(10):
            v, t = fixed_true(filename, n)
            eq_verdicts.append(v)
            eq_times.append(t)
        for i in range(10):
            v,t = fixed_false(filename, n)
            neq_verdicts.append(v)
            neq_times.append(t)
        eq_correctness.append(np.count_nonzero(eq_verdicts) / len(eq_verdicts) * 100)
        neq_correctness.append((len(neq_verdicts) - np.count_nonzero(neq_verdicts)) / len(neq_verdicts) * 100)
        eq_runtimes.append(np.mean(eq_times))
        neq_runtimes.append(np.mean(neq_times))
        eq_min.append(np.min(eq_times))
        neq_min.append(np.min(neq_times))
        eq_max.append(np.max(eq_times))
        neq_max.append(np.max(neq_times))
    return eq_correctness, eq_runtimes, eq_min, eq_max, neq_correctness, neq_runtimes, neq_min, neq_max

def fixed_true(filename, n):
    start_time = time.perf_counter()
    true_eval(filename, n)
    result = eq_fixed_q(filename)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def fixed_false(filename, n):
    start_time = time.perf_counter()
    false_eval(filename, n)
    result = eq_fixed_q(filename)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)