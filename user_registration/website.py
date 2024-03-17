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

from mlsocket import MLSocket
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

# error matrix is generated using normal distribution function
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

def compute_b():
    
    HOST = '127.0.0.1'
    PORT = 65435

    with MLSocket() as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, address = s.accept()
        
        # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
        with conn:
            data = conn.recv(1024) 
    
    # The random matrix a is generated
    start_time = timeit.default_timer()
    
    A = np.random.randint(0,(q)-1,size = (m,n))
     
    
    # user chosen password is mapped into a matrix
    P = password_matrix.compute_password_matrix()
    # K = value of xor of secret key matrix and password matrix
    K = np.bitwise_xor(data, P) 
    K = K%q
    
    bA = np.matmul(A,K)%q
    bA = np.add(bA,eA)%q
    
    end_time = timeit.default_timer()
    total_time = end_time - start_time
    print("Registration Success!!")
    #print("\nTotal time taken in seconds: ", end_time - start_time)
    # Storing the matrices at database
    np.savetxt('../Website_database/A.txt',A) 
    np.savetxt('../Website_database/b.txt',bA) 


def send_error():
    HOST = '127.0.0.1'
    PORT = 65530
    with MLSocket() as e:
        # Connect to the port and host
        e.connect((HOST, PORT)) 
        # After sending the secret key matrix
        e.send(eA) 


if __name__ == '__main__':
    compute_b()
    send_error()
    
