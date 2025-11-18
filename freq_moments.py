# frequency moments: F_2
import math
import random
import numpy as np
import equality.py 
data = [1,2,3,4,5,6,7,8]

#map n-vector into hxv matrix
def map(input1):
    length = len(data)
    h = math.ceil(math.sqrt(length))
    v = h
    matrix = np.zeros(h,v)
    for i in range(0, h):
        matrix[i,:] = input1[i*v:(i+1)*v-1]
def millerRabin(d,q):
    a = 2 + random.randint(1,q - 4)
    x = pow(a,d)
    x = x % q
    if (x == q) or (x == q - 1):
        return True
    while (d != q - 1):
        x = (x * x) % q
        d *= 2

    if (x == 1):
        return False
    if (x == q - 1):
        return True
    return False

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

def pickprime(qmin):
    q = random.randint(qmin, qmin + 100000000)
    while not isprime(q):
        q = random.randint(qmin, qmin + 100000000)
    return q
    
# length of string
n = 4    
# the number of rows in the matrix
h = math.ceil(math.sqrt(n))

def fingerprint():
    m = n + random.randint(1,100000)
    qmin = max(pow(m, k), 3*k*h)
    q = pickprime(qmin)