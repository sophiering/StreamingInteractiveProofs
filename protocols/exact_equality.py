# let's go! :D
import math
import random
import secrets
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
base_path = Path(__file__).resolve().parent.parent

from stream_generation.gen_equality import true_eq, false_eq

#input : an integer n, first string of length n, second string of length n
#output : true or false

#q = random.randint(10000000,100000000)
q = random.randint(10000,100000)
# larger k = more accuracy
k = 45

def equality_t(filename):
    filename = true_eq(filename)
    return exact_equality_check(filename)

def equality_f(filename):
    filename = false_eq(filename)
    return exact_equality_check(filename)

# carries out the Miller-Rabin primality test
def miller_rabin(d,s,q):
    a = random.randint(2,q - 2)
    x = pow(a,d,q)

    if (x == 1) or (x == q - 1):
        return True

    for i in range(s - 1):
        x = pow(x,2,q)
        if x == q - 1:
            return True
    return False

# determines if a number is prime
def prime_check(q, k):
    # edge cases
    if (q == 2) or (q == 3):
        return True
    elif (q < 2) or (q % 2 == 0):
        return False
    
    s = 0
    d = q - 1
    while (d % 2 == 0):
        s += 1
        d //= 2
    # repeak miller-rabin for k rounds
    for _ in range(k):
        if (miller_rabin(d,s,q) == False):
            return False
    return True
    
# generates random number q until q is prime
def pick_prime(qmin, k):
    qmin = int(qmin)
    q = 2 * random.randint(qmin, qmin + 100000000) + 1
    while not prime_check(q, k):
        q = 2 * random.randint(qmin, qmin + 100000000) + 1
    #print("q found")
    return q

# used to stream in the input
def stream_generator(filename):
    filepath = base_path / "streams" / filename
    with open(filepath, 'r') as stream:
        for line in stream:
            yield int(line.strip())

# checkpoint to determine equality
def exact_equality_check(filename): 
    stream = stream_generator(filename)
    # length of the input without annotation
    n = next(stream) 
    # m >= n
    m = n + random.randint(0,60)
    # the number of rows in the matrix
    h = math.ceil(math.sqrt(n))
    # pick a prime from 1 to M 
    qmin = max(pow(m, k), 3*k*h)
    q = pick_prime(qmin, k)
    # calculate lagragian interpolating polynomial at this point
    r = secrets.randbelow(q) 
    # fingerprint of stream 1
    fp1 = 0
    # fingerprint of stream 2
    fp2 = 0
    x_term = 1
    for _ in range(n):
        a_i = next(stream)
        fp1 = (fp1 + a_i * x_term) % q
        x_term = (x_term * r) % q
    x_term = 1
    for _ in range(n):
        try:
            b_i = next(stream)
            fp2 = (fp2 + b_i * x_term) % q
            x_term = (x_term * r) % q
        except ValueError:
            print("length of inputs aren't equal")
            return False
    # WE MUST MAKE SURE LENGTH > n IS ALSO REJECTED
    try:
        b_i = next(stream)
        print("length of inputs aren't equal")
        return False
    except ValueError:
        if fp1 == fp2:
            return True
        else:
            print("fingerprints aren't equal")
            return False
    
def exact_fixed_q(filename): 
    stream = stream_generator(filename)
    # length of the input without annotation
    n = next(stream) 
    # fixed q chosen
    q = 2305843009213693951
    # calculate lagragian interpolating polynomial at this point
    r = secrets.randbelow(q) 
    # fingerprint of stream 1
    fp1 = 0
    # fingerprint of stream 2
    fp2 = 0
    x_term = 1
    for i in range(n):
        a_i = next(stream)
        fp1 = (fp1 + a_i * x_term) % q
        x_term = (x_term * r) % q
    x_term = 1
    for i in range(n):
        try:
            b_i = next(stream)
            fp2 = (fp2 + b_i * x_term) % q
            x_term = (x_term * r) % q
        except ValueError:
            print("length of inputs aren't equal")
            return False
    # WE MUST MAKE SURE LENGTH > n IS ALSO REJECTED
    try:
        b_i = next(stream)
        print("length of inputs aren't equal")
        return False
    except StopIteration:
        if fp1 == fp2:
            return True
        else:
            print("fingerprints aren't equal")
            return False