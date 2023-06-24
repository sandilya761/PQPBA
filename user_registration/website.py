'''
Website.py is the file where we assume that a user registers his username and password at website.
As per protocol 1 mentioned in the paper, website contacts the secure server (secure_server.py) and
obtains the secret key (sA) required to compute the lwe instance (b).

Parameters of the LWE problem: 

    A  (random matrix):- m x n
    eA (error matrix) :- m x 1
    sA (secret key matrix) :- n x 1
    bA (final matrix) :- m x 1
    P (password matrix) :- n x 1
    q  :- size of the field contains elements from {0,....,q-1}
    m:- number of equations
    n:- number of variables

Values of m and n are taken as per paper "Frodo: Take off the ring!
Practical, Quantum-Secure Key Exchange from LWE"
'''

from mlsocket import MLSocket
import numpy as np
import sys
from numpy import random
import timeit
import password_matrix

# Initialize the values of m and n respectively.
m = 752
n = 752

# error matrix is generated using normal distribution function
q = 2**15 # value of q (field size) for computing the lwe problem.
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

def compute_b():
    
    HOST = '127.0.0.1'
    PORT = 65435

    with MLSocket() as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, address = s.accept()
        start_time = timeit.default_timer()
        
        # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
        with conn:
            data = conn.recv(1024) 
    #print("Secret key obtained from secure server: \n",data)
    
    # The random matrix a is generated
    A = np.random.randint(0,(2**15)-1,size = (m,n))
     
    
    # user chosen password is mapped into a matrix
    P = password_matrix.compute_password_matrix()
    # K = value of xor of secret key matrix and password matrix
    K = np.bitwise_xor(data, P) 

    
    bA = np.matmul(A,K)%q
    bA = np.add(bA,eA)%q
    #print("\nValue of b: \n",bA)
    
    end_time = timeit.default_timer()
    total_time = end_time - start_time
    print("\nTotal time taken in seconds: ", end_time - start_time)
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
    
