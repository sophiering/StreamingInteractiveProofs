import random
import numpy as np

def true_f2_2d(filename):
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    # h = 
    with open(filename, "w") as f:
        f.write(f"{n}\n")
    with open(filename, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
        np.savetxt(f, h, fmt = '%d')
    return filename

def false_f2_2d(filename):
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    # h = 
    with open(filename, "w") as f:
        f.write(f"{n}\n")
    with open(filename, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
        np.savetxt(f, h, fmt = '%d')
    return filename


def f2_3d():
    pass