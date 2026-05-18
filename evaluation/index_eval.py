import tracemalloc
import numpy as np 
import time
import sys
import secrets
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.index import verifier, compute_g, check_g
from protocols.index_multivariate import m_verifier, HonestProver, DishonestProver, m_check_g
from protocols.honest_v_zk_index import honest_verifier, HVZKHonestProver, HVZKDishonestProver, fingerprint, check_g_zk
from protocols.zk_index import ZKHonestProver, ZKDishonestProver, temporal_commitment, temporal_decommitment, d_verifier, h_verifier
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
    # keep track of memory
    tracemalloc.start()
    a, true_a_j = index_eval(filename,n)
    F_q, mu, r, sketch, n, h, a_j = verifier(filename)
    g = compute_g(a, a_j, mu, r, n, h, F_q)
    result = check_g(sketch, g, mu, F_q)
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats[:5]:
        print(stat) 
    if result == true_a_j:
        # correctly finds a_j
        result = 1
    else:
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def index_f_eval(filename, n):
    start_time = time.perf_counter()
    tracemalloc.start()
    a, _ = index_eval(filename,n)
    F_q, mu, r, sketch, n, h, a_j = verifier(filename)
    g = compute_g(a, a_j, mu, r, n, h, F_q)
    g = np.random.permutation(g)
    result = check_g(sketch, g, mu, F_q)
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats[:5]:
        print(stat) 
    if result == False:
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
    prover = HonestProver(a, a_j, n, h, F_q, dim)
    g = prover.compute_g(mu, r)
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
    prover = DishonestProver(a, a_j, n, h, F_q, dim)
    g = prover.compute_g(mu, r)
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

def eval_honest_v_index(filename, dim, n_vals):
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
            v, t = honest_v_t_eval(filename, dim, n)
            honest_verdicts.append(v)
            honest_times.append(t)
        # dishonest prover tests
        for i in range(10):
            v, t = honest_v_f_eval(filename, dim, n)
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

def honest_v_t_eval(filename, dim, n):
    q = 65537
    start_time = time.perf_counter()
    a, true_a_j = index_eval(filename,n)
    F_q, mu, r, mapped_r, sketch, n, h, a_j = honest_verifier(filename, q, dim)
    prover = HVZKHonestProver(a, a_j, n, h, F_q, dim)
    p = 100 + secrets.randbelow(1000)
    g_0, commit, deg_g = prover.m_compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    unlocked_evals = prover.algebraic_decommitment(y,k) 
    if check_g_zk(F_q, mu, sketch, g_0, gamma, k, unlocked_evals, folded_gamma, fp, beta, folded_y, sigma) == true_a_j:
        # correctly finds a_j
        result = 1
    else:
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def honest_v_f_eval(filename, dim, n):
    q = 65537
    start_time = time.perf_counter()
    a, true_a_j = index_eval(filename,n)
    F_q, mu, r, mapped_r, sketch, n, h, a_j = honest_verifier(filename, q, dim)
    prover = HVZKDishonestProver(a, a_j, n, h, F_q, dim)
    p = 100 + secrets.randbelow(1000)
    g_0, commit, deg_g = prover.m_compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    unlocked_evals = prover.algebraic_decommitment(y,k) 
    if check_g_zk(F_q, mu, sketch, g_0, gamma, k, unlocked_evals, folded_gamma, fp, beta, folded_y, sigma) == False:
        # correctly terminated
        result = 1
    else:
        # did not terminate
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def eval_zk_index(filename, dim, n_vals):
    honest_correctness =[]
    dishonest_p_correctness = []
    dishonest_v_correctness = []
    honest_runtimes = []
    dishonest_p_runtimes = []
    dishonest_v_runtimes = []
    honest_min = []
    dishonest_p_min = []
    dishonest_v_min = []
    dishonest_min = []
    honest_max = []
    dishonest_p_max = []
    dishonest_v_max = []
    for n in n_vals:
        honest_verdicts = []
        dishonest_p_verdicts = []
        dishonest_v_verdicts = []
        honest_times = []
        dishonest_p_times = []
        dishonest_v_times = []
        # honest prover tests
        for i in range(10):
            v, t = zk_t_eval(filename, dim, n)
            honest_verdicts.append(v)
            honest_times.append(t)
        # dishonest prover tests
        for i in range(10):
            v, t = zk_d_p_eval(filename, dim, n)
            dishonest_p_verdicts.append(v)
            dishonest_p_times.append(t)
        # dishonest prover tests
        for i in range(10):
            v, t = zk_d_v_eval(filename, dim, n)
            dishonest_v_verdicts.append(v)
            dishonest_v_times.append(t)
        honest_correctness.append(np.count_nonzero(honest_verdicts) / len(honest_verdicts) * 100)
        dishonest_p_correctness.append(np.count_nonzero(dishonest_p_verdicts) / len(dishonest_p_verdicts) * 100)
        dishonest_v_correctness.append(np.count_nonzero(dishonest_v_verdicts) / len(dishonest_v_verdicts) * 100)
        honest_runtimes.append(np.mean(honest_times))
        dishonest_p_runtimes.append(np.mean(dishonest_p_times))
        dishonest_v_runtimes.append(np.mean(dishonest_v_times))
        honest_min.append(np.min(honest_times))
        dishonest_p_min.append(np.min(dishonest_p_times))
        dishonest_v_min.append(np.min(dishonest_v_times))
        honest_max.append(np.max(honest_times))
        dishonest_p_max.append(np.max(dishonest_p_times))
        dishonest_v_max.append(np.max(dishonest_v_times))
    return honest_correctness, honest_runtimes, honest_min, honest_max, dishonest_p_correctness, dishonest_p_runtimes, dishonest_p_min, dishonest_p_max, dishonest_v_correctness, dishonest_v_runtimes, dishonest_v_min, dishonest_v_max


def zk_t_eval(filename, dim, n):
    start_time = time.perf_counter()
    a, true_a_j = index_eval(filename,n)
    q = 65537
    # create the stream
    prover = ZKHonestProver(a, dim, q)
    # send perm F_q
    perm = prover.perm_F_q()
    # verifier temporal commitment
    r, index = temporal_commitment(perm, q)
    #verifer creates its sketch
    F_q, mu, r, mapped_r, sketch, n, h, a_j = h_verifier(filename, q, dim, r)
    # prover observe
    prover.observe(a_j, n, h, F_q)
    # algebraic commitment
    p = 100 + secrets.randbelow(1000)
    # prover calculates the g vals
    g_0, commit, deg_g = prover.compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    # temporal decommitment
    if temporal_decommitment(perm, r, index) == False:
        return False
    # algebraic decommitment
    unlocked_evals = prover.algebraic_decommitment(y,k) 
    if check_g_zk(F_q, mu, sketch, g_0, gamma, k, unlocked_evals, folded_gamma, fp, beta, folded_y, sigma) == true_a_j:
        # correctly finds a_j
        result = 1
    else:
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def zk_d_p_eval(filename, dim, n):
    start_time = time.perf_counter()
    a, _ = index_eval(filename,n)
    q = 65537
    # create the stream
    prover = ZKDishonestProver(a, dim, q)
    # send perm F_q
    perm = prover.perm_F_q()
    # verifier temporal commitment
    r, index = temporal_commitment(perm, q)
    #verifer creates its sketch
    F_q, mu, r, mapped_r, sketch, n, h, a_j = h_verifier(filename, q, dim, r)
    # prover observe
    prover.observe(a_j, n, h, F_q)
    # algebraic commitment
    p = 100 + secrets.randbelow(1000)
    # prover calculates the g vals
    g_0, commit, deg_g = prover.compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    # temporal decommitment
    if temporal_decommitment(perm, r, index) == False:
        return False
    # algebraic decommitment
    unlocked_evals = prover.algebraic_decommitment(y,k) 
    if check_g_zk(F_q, mu, sketch, g_0, gamma, k, unlocked_evals, folded_gamma, fp, beta, folded_y, sigma) == False:
        # correctly terminated
        result = 1
    else:
        # did not terminate
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)

def zk_d_v_eval(filename, dim, n):
    start_time = time.perf_counter()
    a, _ = index_eval(filename,n)
    q = 65537
    # create the stream
    prover = ZKHonestProver(a, dim, q)
    # send perm F_q
    perm = prover.perm_F_q()
    # verifier temporal commitment
    temporal_commitment(perm, q)
    #verifer creates its sketch of big ole nothing
    F_q, mu, r, mapped_r, sketch, n, h, a_j, index = d_verifier(filename, q, dim)
    # prover observe
    prover.observe(a_j, n, h, F_q)
    # algebraic commitment
    p = 100 + secrets.randbelow(1000)
    # prover calculates the g vals
    g_0, commit, deg_g = prover.compute_g(mu, mapped_r, p)
    y, gamma, k = commit
    folded_gamma, fp, beta, folded_y, sigma = fingerprint(r, y, gamma, k, deg_g, F_q)
    # temporal decommitment should correctly terminate
    if temporal_decommitment(perm, r, index) == False:
        print("malicious verifier")
        result = 1
    else:
        # did not terminate
        result = 0
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (result, run_time)