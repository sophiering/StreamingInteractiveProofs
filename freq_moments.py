# frequency moments: F_2
import math
import random
import numpy as np
from equality.py import pickprime, millerRabin, isprime
data = [1,2,3,4,5,6,7,8]

#map n-vector into hxv matrix
def map(input1):
    length = len(input1)
    h = math.ceil(math.sqrt(length))
    v = h
    matrix = np.zeros(h,v)
    padded = input1 + [0] * (h*v - input1)
    for i in range(0, h):
        if (v == h):
            matrix[i,:] = input1[i*v:(i+1)*v-1]


def isprime(q, k):
    #edge cases
    if (q == 2):
        return True
    elif (q < 2) or (q % 2 == 0):
        return False
    
    d = q - 1
    while (d % 2 == 0):
        d //= 2

    for i in range(k):
        if (millerRabin(d,q) == False):
            return False

    return True
    
# length of string
n = 4    
# the number of rows in the matrix
h = math.ceil(math.sqrt(n))
# larger k = more accuracy
k = 45

def fingerprint(n,k,h):
    m = n + random.randint(1,100000)
    qmin = max(pow(m, k), 3*k*h)
    q = pickprime(qmin)


