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



# value of q is taken as 2**16for computing the lwe problem

q = 8191

# value of m, n, l
m = 192
n = 192
l = 80

# empty list to store all the values of b
l_b = [] 
for i in range(0,100):
    
    # The random matrix a is generated

    A = np.random.randint(0,(q)-1,size = (m,m))
    start_time = timeit.default_timer() 
    # secret key matrix is generated
    sA = np.random.randint(0,(q)-1,size = (n,l)) 
    # error matrix 
    # Set the desired range for the normal distribution
    lower_bound = -q/4
    upper_bound = q/4

    # Set the mean and standard deviation of the normal distribution
    mean = 0
    std_dev = 1
    # Generate random numbers from the normal distribution
    eA = np.random.normal(mean, std_dev, size=(m,l))

    # Truncate the random numbers to the desired range
    eA = np.clip(eA, lower_bound, upper_bound)

    # user chosen password is mapped into a matrix 
    
    P = password_matrix.compute_password_matrix()
    #print(P)
    
    # K = value of xor of secret key matrix and password matrix
    K = np.bitwise_xor(sA,P) 
    
    
    bA = np.matmul(A,K)%q

    bA = np.add(bA,eA)%q
    
    end_time = timeit.default_timer()
    t = end_time - start_time
    np.savetxt('A.txt',A)
    np.savetxt('b.txt',bA)
    np.savetxt('error.txt',eA)
    np.savetxt('secret_key.txt',sA)
    
    
    l_b.append(t)
g = sum(l_b)/100

# prints the total time taken to run the program.
print("time in milliseconds: ",g*1000)
