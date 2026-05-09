import sys
import numpy as np
import math
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from protocols.equality import equality_check
from stream_generation.gen_freq_moments import f_2_s, f_2_h_2d_t, f_2_h_2d_f

k = 45

def eval_eq(filename):
    filepath = base_path / "streams" / filename
    n_vals = [int(math.pow(2,10)), int(math.pow(2,15)), int(math.pow(2,20))]
    t_correctness = []
    f_correctness = []
    t_runtimes = []
    f_runtimes = []
    for n in n_vals:
        t_vals = []
        f_vals = []
        t_times = []
        f_times = []
        for i in range(5):
            f_2_s(filepath)
            # correct helper functino
            t_val, t_time = f_2_h_2d_t(filepath, k)
            if t_val == -1:
                t_vals.append(0)
            else: 
                t_vals.append(1)
            t_times.append(t_time)
            # bad helper function
            f_val, f_time = f_2_h_2d_f(filepath, k)
            if f_val == -1:
                f_vals.append(0)
            else:
                f_vals.append(1)
            f_times.append(f_time)
        print(t_vals)
        print(f_vals)
        t_correctness.append(np.count_nonzero(t_vals) / len(t_vals) * 100)
        f_correctness.append((len(f_vals) - np.count_nonzero(f_vals)) / len(f_vals) * 100)
        t_runtimes.append(np.mean(t_times))
        f_runtimes.append(np.mean(f_times))
    return t_correctness, t_runtimes, f_correctness, f_runtimes

