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
import inv
from operator import matmul



# value of q = 2**16 for computing the lwe problem
#q=8380417

q=8191

# value of m and n
m = 192
n = 192
l = 80

# empty list to store all the values of b
l_b = [] 
for i in range(0,1):
    
    # The random matrix A is generated
    A = np.loadtxt('A.txt')
    A = A.astype(int)
    
    # loads the value of matrix b 
    b = np.loadtxt('b.txt')
    b = b.astype(float)
    bA = b.reshape((m,l))


    # old secret key matrix is loaded
    
    old_sa = np.loadtxt('secret_key.txt')
    old_sa = old_sa.astype(int)
    old_sA = old_sa.reshape((n,l))

    # error matrix 
    # Set the desired range for the normal distribution
    ea = np.loadtxt('error.txt')
    ea = ea.astype(float)
    eA = ea.reshape((m,l))

    
    start_time = timeit.default_timer()
    # new matrix is created
    new_sA = np.random.randint(0,(q)-1,size = (n,l))
    # new matrix is xored with old one
    sA = np.bitwise_xor(old_sA,new_sA)


    # user chosen password is mapped into a matrix 
    P = password_matrix.compute_password_matrix()

    # compute inverse of matrix A
    inv_a = inv.inversematrix(A,q)

    x = np.subtract(bA%q,eA%q) # (b-e) mod q
    x = x%q
    
    x = matmul(inv_a,x)
    final = x%q # final = secret value xor password = K
    # convert the float value to int 
    final = final.astype(int)
    final = final.reshape((m,l))
    
    # received sA = old_sA xor new_sA. So, sA xor old_sA xor password = new_sA xor Password
    K_new = np.bitwise_xor(sA,final)
    # new value of b is computed
    b_new = np.matmul(A,K_new)%q
    b_new = np.add(b_new,eA)%q
    #print("b value changed successfully")
    end_time = timeit.default_timer()
    t = end_time - start_time
    l_b.append(t)

g = sum(l_b)/1
print("time in seconds: ",g)
