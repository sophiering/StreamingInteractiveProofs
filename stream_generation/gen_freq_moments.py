import random
import numpy as np
import math
import galois as g

from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

def f_s(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    with open(filepath, "w") as f:
        np.savetxt(f, s, fmt = '%d')
    # n is used to verify 
    return n

def f_1_test(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    f_1 = np.sum(s)
    with open(filepath, "w") as f:
        np.savetxt(f, s, fmt = '%d')
    # n is used to verify 
    return f_1

def f_2_s(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
    return n, s

def f_2_eval(filename, n):
    filepath = base_path / "streams" / filename
    s = np.random.randint(0, 1000000, size = n)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
    return s