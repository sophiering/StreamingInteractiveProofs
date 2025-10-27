# let's go! :D
import math
import random

input1 = [1,2,3,4] # input()
input2 = [1,2,3,4] # input() 

def equality(input1, input2): #checkpoint
    l = len(input1)
    # for stream 1 and 2:
    # calculate lagragian interpolating polynomial
    checkpoint = random.uniform(0,l) 
    total1 = 0
    total2 = 0
    for i in range(0,l): 
        xi = 1
        for j in range(0,l):
            if j != i:
                xi *= (checkpoint - j)/(i - j)
        total1 += input1[i] * xi
        total2 += input2[i] * xi
    # evaluate polynomials 1 and 2 at random point x
    # if equal (to small precision) then equal (output the value @ x) else not (output False)
    if math.isclose(total1, total2) == True:
        print(str(total1))
    else:
        print("False")


