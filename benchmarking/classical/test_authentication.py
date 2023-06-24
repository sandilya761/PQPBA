'''
This is a basic implementation of our PQPBA scheme which is based on LWE problem.
General LWE problem is as follows : b = (<a,s> + e )mod q. But in our scheme we replace matrix s with s xor p. where p is the
user chosen password. 
Hence, the modified LWE problem is as follows: b = (<a,K> + e) mod q ; K = s xor P.

Parameters of the LWE problem: 

    A :- m x n
    e :- m x 1
    s :- n x 1
    b :- m x 1
    q :- size of the field contains elements from {0,....,q-1}
    m:- number of equations
    n:- number of variables

'''
import numpy as np
import sys
from numpy import random
import timeit
import password_matrix



# value of q for computing the lwe problem is picked at random

q=2**12
#print("Value of q\n",q)

# value of m and n
m = 592
n = 592

# empty list to store all the values of b
l_b = [] 
for i in range(0,10000):
    
    # The random matrix a is generated
    A = np.loadtxt('A.txt')
    A = A.astype(int)
    #print(A.shape)
    #print("Value of random matrix A is: \n",A)

    # secret key matrix is generated
    sa = np.loadtxt('secret_key.txt')
    sa = sa.astype(int)
    sA = sa.reshape((n,1))
    # error matrix 
    # Set the desired range for the normal distribution
    ea = np.loadtxt('error.txt')
    ea = ea.astype(float)
    eA = ea.reshape((m,1))

    # load bA matrix
    ba = np.loadtxt('b.txt')
    ba = ba.astype(float)
    bA = ba.reshape((m,1))
    start_time = timeit.default_timer()

    # user chosen password is mapped into a matrix 
    P = password_matrix.compute_password_matrix()
    
    # K = value of xor of secret key matrix and password matrix
    K = np.bitwise_xor(sA,P) 
    #print("Value of sA xor password: ",K) 
    #print("size of secret key: ",K.size)
    bA_new = np.matmul(A,K)%q

    bA_new = np.add(bA_new,eA)%q
    
    if (bA==bA_new).all():
        print("Authentication success!!")

    else:
        print("Authentication Failed!!")
    
    #print ("Print output\n",bA.size)

    end_time = timeit.default_timer()
    l_b.append(end_time - start_time)
#print(len(l_b))

# prints the total time taken to run the program.
print(sum(l_b)/10000)
#print("Total time taken in seconds: ",end_time - start_time)
