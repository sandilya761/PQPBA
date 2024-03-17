'''
This is a basic implementation of our PQPBA scheme which is based on LWE problem.
General LWE problem is as follows : b = (a.s + e )mod q. But in our scheme we replace matrix s with s xor p. where p is the
user chosen password. 
Hence, the modified LWE problem is as follows: b = (a.K + e) mod q ; K = s xor P.

Parameters of the LWE problem: 

    A :- m x n
    e :- m x l
    s :- n x l
    b :- m x l
    q :- size of the field contains elements from {0,....,q-1}
    m:- number of equations
    n:- number of variables

'''
import numpy as np
import sys
from numpy import random
import timeit
import password_matrix
import multiprocessing as mp


# value of q = 2**16 for computing the lwe problem

q=8191

# value of m and n
m = 192
n = 192
l = 80

# empty list to store all the values of b
l_b = []

for i in range(0,100):
        
    # The matrix A is loaded from the database
    A = np.loadtxt('A.txt')
    A = A.astype(int)
    

    # secret key matrix is loaded from the database
    sa = np.loadtxt('secret_key.txt')
    sa = sa.astype(int)
    sA = sa.reshape((n,l))
    # error matrix is loaded from the database 
    
    ea = np.loadtxt('error.txt')
    ea = ea.astype(float)
    eA = ea.reshape((m,l))

    # matrix b is loaded
    ba = np.loadtxt('b.txt')
    ba = ba.astype(float)
    bA = ba.reshape((m,l))

    start_time = timeit.default_timer()
    # user chosen password is mapped into a matrix 
    P = password_matrix.compute_password_matrix()
        
    # K = value of xor of secret key matrix and password matrix
    K = np.bitwise_xor(sA,P) 

    # computes bA_new value based on the inputs
    bA_new = np.matmul(A,K)%q

    bA_new = np.add(bA_new,eA)%q
    # compares the computed bA value with the one stored in database
    #if (bA==bA_new).all():
    #    print("Authentication success!!")

    #else:
    #    print("Authentication Failed!!")
        
    

    end_time = timeit.default_timer()
    
    t = end_time - start_time
    l_b.append(t)

g = sum(l_b)/100
# prints the total time taken to run the program.
print("Time in milliseconds: ",g*1000)

