import math 
import random
import numpy as np 
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from protocols.equality import equality_check

def gen_stream(n, filename):
    a = np.random.randint(0, 1000000, size = n)
    with open(filename, "w") as f:
        f.write(f"{n}\n")
    with open(filename, "ab") as f:
        np.savetxt(f, a, fmt = '%d')
        if random.randint(0,1) == 1:
            np.savetxt(f, a, fmt = '%d')
        else: 
            b = np.random.permutation(a)
            np.savetxt(f,b,fmt = '%d')
    return filename

def eval_eq(filename):
    n_vals = [int(math.pow(2,10)), int(math.pow(2,15)), int(math.pow(2,20))]
    run_times = []
    for n in n_vals:
        n_times = []
        for i in range(10):
            gen_stream(n, filename)
            _, t = equality_check(filename)
            n_times.append(t)
        run_times.append(n_times)
    print(True)
