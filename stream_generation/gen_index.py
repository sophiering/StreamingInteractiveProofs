import random
import numpy as np

from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

def gen_index(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    a = np.random.randint(0, 1000000, size = n)
    j = random.randint(1, n)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
        for element in a:
            f.write(f"{int(element)}\n")
        f.write(f"{j}\n")
    return a

def index_test(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    a = np.random.randint(0, 1000000, size = n)
    j = random.randint(1, n)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
        for element in a:
            f.write(f"{int(element)}\n")
        f.write(f"{j}\n")
    return a, a[j]

def fixed_test(filename, contents):
    filepath = base_path / "streams" / filename
    with open(filepath, "w") as f:
        for element in contents:
            f.write(f"{int(element)}\n")
    return filename