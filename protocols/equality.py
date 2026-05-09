# let's go! :D
import math
import random
import time
import secrets

from pathlib import Path
from stream_generation.gen_equality import true_eq, false_eq

base_path = Path(__file__).resolve().parent.parent

#input : an integer n, first string of length n, second string of length n
#output : true or false

#q = random.randint(10000000,100000000)
q = random.randint(10000,100000)
# larger k = more accuracy
k = 45

def equality_t(filename):
    filename = true_eq(filename)
    return equality_check(filename)

def equality_f(filename):
    filename = false_eq(filename)
    return equality_check(filename)

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
    start_time = time.perf_counter()
    # edge cases
    if (q == 2) or (q == 3):
        end_time = time.perf_counter()
        run_time = end_time - start_time
        return (True, run_time)
    elif (q < 2) or (q % 2 == 0):
        end_time = time.perf_counter()
        run_time = end_time - start_time
        return (False, run_time)
    
    s = 0
    d = q - 1
    while (d % 2 == 0):
        s += 1
        d //= 2

    for i in range(k):
        if (miller_rabin(d,s,q) == False):
            end_time = time.perf_counter()
            run_time = end_time - start_time
            return (False, run_time)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    return (True, run_time)
    
# generates random number q until q is prime
def pick_prime(qmin, k):
    q = 2 * random.randint(qmin, qmin + 100000000) + 1
    while not prime_check(q, k):
        q = 2 * random.randint(qmin, qmin + 100000000) + 1
    #print("q found")
    return q

def stream_generator(filename):
    filepath = base_path / "streams" / filename
    with open(filepath, 'r') as stream:
        for line in stream:
            yield int(line.strip())

# checkpoint to determine equality
def equality_check(filename): 
    start_time = time.perf_counter()
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
    checkpoint = secrets.randbelow(q) 

    # fingerprint of stream 1
    fp1 = 0
    # fingerprint of stream 2
    fp2 = 0
    x_term = 1
    # time - we could just use this start time metric !
    t = 0
    for i in range(n):
        i1 = next(stream)
        fp1 = (fp1 + i1 * x_term) % q
        x_term = (x_term * checkpoint) % q
        # are we using this?
        t += 1
    x_term = 1
    for i in range(n):
        try:
            i2 = next(stream)
            fp2 = (fp2 + i2 * x_term) % q
            x_term = (x_term * checkpoint) % q
            # are we using this?
            t += 1
        except ValueError:
            print("length of inputs aren't equal")
            end_time = time.perf_counter()
            run_time = end_time - start_time
            return (False, run_time)
    # WE MUST MAKE SURE LENGTH > n IS ALSO REJECTED

    if fp1 == fp2:
        end_time = time.perf_counter()
        #runtime
        run_time = end_time - start_time
        return (True, run_time)
    else:
        end_time = time.perf_counter()
        #runtime
        run_time = end_time - start_time
        return (False, run_time)