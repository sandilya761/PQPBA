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

q=8380417
#print("Value of q\n",q)

# value of m and n
m = 256
n = 256

# empty list to store all the values of b
l_b = [] 
for i in range(0,1):
    start_time = timeit.default_timer()
    # The random matrix a is generated

    A = np.random.randint(0,(q)-1,size = (m,n))
     

    #print("Value of random matrix A is: \n",A)

    # secret key matrix is generated
    sA = np.random.randint(0,(q)-1,size = (n,1)) 
    # error matrix 
    # Set the desired range for the normal distribution
    lower_bound = -q/4
    upper_bound = q/4

    # Set the mean and standard deviation of the normal distribution
    mean = 0
    std_dev = 1
    # Generate random numbers from the normal distribution
    eA = np.random.normal(mean, std_dev, size=(m,1))

    # Truncate the random numbers to the desired range
    eA = np.clip(eA, lower_bound, upper_bound)

    # user chosen password is mapped into a matrix 
    P = password_matrix.compute_password_matrix()
    
    # K = value of xor of secret key matrix and password matrix
    K = np.bitwise_xor(sA,P) 
    #print("Value of sA xor password: ",K) 
    #print("size of secret key: ",K.size)
    bA = np.matmul(A,K)%q

    bA = np.add(bA,eA)%q
    #print(bA)
    
    #print ("Print output\n",bA.size)
    np.savetxt('A.txt',A)
    np.savetxt('b.txt',bA)
    np.savetxt('error.txt',eA)
    np.savetxt('secret_key.txt',sA)
    end_time = timeit.default_timer()
    l_b.append(end_time - start_time)
    
#print(len(l_b))

# prints the total time taken to run the program.
print(sum(l_b)/1)
#print("Total time taken in seconds: ",end_time - start_time)
