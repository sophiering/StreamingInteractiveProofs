import random
import numpy as np

def true_eq(filename):
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    with open(filename, "w") as f:
        f.write(f"{n}\n")
    with open(filename, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
        np.savetxt(f, s, fmt = '%d')
    return filename

def false_eq(filename):
    n = random.randint(1, 1000000)
    a = np.random.randint(0, 1000000, size = n)
    b = np.random.permutation(a)
    with open(filename, "w") as f:
        f.write(f"{n}\n")
    with open(filename, "ab") as f:
        np.savetxt(f, a, fmt = '%d')
        np.savetxt(f, b, fmt = '%d')
    return filename




