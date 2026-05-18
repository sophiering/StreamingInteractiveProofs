import random
import numpy as np

from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

def true_eq(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
        np.savetxt(f, s, fmt = '%d')
    return filename

def perm_eq(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    a = np.random.randint(0, 1000000, size = n)
    b = np.random.permutation(a)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, a, fmt = '%d')
        np.savetxt(f, b, fmt = '%d')
    return filename

def false_eq(filename):
    filepath = base_path / "streams" / filename
    n = random.randint(1, 1000000)
    a = np.random.randint(0, 1000000, size = n)
    b = np.random.permutation(a) 
    a[0] += 1
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, a, fmt = '%d')
        np.savetxt(f, b, fmt = '%d')
    return filename

def gen_test(filename, input1, input2):
    filepath = base_path / "streams" / filename
    with open(filepath, "w") as f:
        f.write(f"{len(input1)}\n")
        for element in input1:
            f.write(f"{int(element)}\n")
        for element in input2:
            f.write(f"{int(element)}\n")
    return filename

def true_eval(filename, n):
    filepath = base_path / "streams" / filename
    s = np.random.randint(0, 1000000, size = n)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
        np.savetxt(f, s, fmt = '%d')
    return filename

def perm_eval(filename, n):
    filepath = base_path / "streams" / filename
    a = np.random.randint(0, 1000000, size = n)
    b = np.random.permutation(a)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, a, fmt = '%d')
        np.savetxt(f, b, fmt = '%d')
    return filename

def false_eval(filename, n):
    filepath = base_path / "streams" / filename
    a = np.random.randint(0, 1000000, size = n)
    b = np.random.permutation(a)
    with open(filepath, "w") as f:
        f.write(f"{n}\n")
    with open(filepath, "ab") as f:
        np.savetxt(f, a, fmt = '%d')
        np.savetxt(f, b, fmt = '%d')
    return filename




