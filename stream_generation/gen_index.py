import random
import numpy as np

def gen_index(filename):
    n = random.randint(1, 1000000)
    s = np.random.randint(0, 1000000, size = n)
    j = random.randint(1, 1000000)
    with open(filename, "w") as f:
        f.write(f"{n}\n")
    with open(filename, "ab") as f:
        np.savetxt(f, s, fmt = '%d')
    with open(filename, "w") as f:
        f.write(f"{j}\n")
    return filename