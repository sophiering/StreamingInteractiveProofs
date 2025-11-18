# let's go! :D
import math
import random

input1 = [1,2,3,4] # input()
input2 = [1,2,3,4] # input() 

q = random.randint(10000000,100000000)
# larger k = more accuracy
k = 45

# def agrawalKayalSaxena():

def millerRabin(d,s,q):
    a = 2 + random.randint(1,q - 4)
    x = pow(a,d,q)
    for i in range(s):
        y = pow(x,2,q)
        if (y == 1) and (x!= 1) and (x != q - 1):
            return False
        x = y
    if (y != 1):
        return False
    return True

def isprime(q, k):
    #edge cases
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
        if (millerRabin(d,s,q) == False):
            return False

    return True
    
# length of string
N = 4    



def equality(input1, input2): #checkpoint
    #pick a prime from 1 to M 
    qmin = max(pow(m, k), 3*k*h)
    q = pickprime()
    # for stream 1 and 2:
    # calculate lagragian interpolating polynomial
    checkpoint = random.uniform(0,N) 
    total1 = 0
    total2 = 0
    indice = -1
    for i in input1: 
        indice += 1
        xi = 1
        indicej = -1
        for j in input1:
            indicej += 1 
            if j != i:
                xi *= (checkpoint - indicej)/(indice - indicej)
        total1 += input1[indice] * xi
        # check len(1) = len(2)
        try:
            total2 += input2[indice] * xi
        except IndexError:
            return(False)
        
    try:
        input2[indice+1]
        return(False)
    except IndexError:
            # evaluate polynomials 1 and 2 at random point x
            # if equal (to small precision) then equal (output the value @ x) else not (output False)
            if math.isclose(total1, total2) == True:
                print(str(total1))
                return(str(total1))
            else:
                print("False")
                return(False)



