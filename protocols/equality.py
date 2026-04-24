# let's go! :D
import math
import random
import time

#input : an integer n, first string of length n, second string of length n
#output : true or false

#q = random.randint(10000000,100000000)
q = random.randint(10000,100000)
# larger k = more accuracy
k = 45

# carries out the Miller-Rabin primality test
def miller_rabin(d,s,q):
    a = 2 + random.randint(1,q - 4)
    x = pow(a,d,q)
    for i in range(s):
        y = pow(x,2,q)
        if (y == 1) and (x!= 1) and (x != q):
            return False
        x = y
    return True

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

    for i in range(k):
        if (miller_rabin(d,s,q) == False):
            return False
    return True
    
# generates random number q until q is prime
def pick_prime(qmin, k):
    q = random.randint(qmin, qmin + 100000000)
    while not prime_check(q, k):
        q = random.randint(qmin, qmin + 100000000)
    return q



# checkpoint to determine equality
def equality_check(filename): 
    start_time = time.perf_counter()

    with open(filename, 'r') as input:
        # length of string
        n = int(input.readline().strip())
        print(n)
        # m >= n
        m = n + random.randint(0,60)
        # the number of rows in the matrix
        h = math.ceil(math.sqrt(n))
        # pick a prime from 1 to M 
        qmin = max(pow(m, k), 3*k*h)
        q = pick_prime(qmin, k)
        # calculate lagragian interpolating polynomial at this point
        checkpoint = random.randint(0,q-1) 

        # fingerprint of stream 1
        fp1 = 0
        # fingerprint of stream 2
        fp2 = 0
        x_term = 1
        # time - we could just use this start time metric !
        t = 0
        for i in range(n):
            i1 = int(input.readline().strip()) 
            fp1 = (fp1 + i1 * x_term) % q
            x_term = (x_term * checkpoint) % q
            # are we using this?
            t += 1
        x_term = 1
        for i in range(n):
            try:
                i2 = int(input.readline().strip()) 
                fp2 = (fp2 + i2 * x_term) % q
                x_term = (x_term * checkpoint) % q
                # are we using this?
                t += 1
            except ValueError:
                print("length of inputs aren't equal")
                end_time = time.perf_counter()
                # print runtime
                print(end_time - start_time)
                return False
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