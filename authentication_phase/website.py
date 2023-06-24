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

# Initialize the value of m and n 
m = 752
n = 752


def compute_b():
    # matrices are loaded from the database.
    # The matrix A is loaded from the database (A.txt)
    A = np.loadtxt('../Website_database/A.txt')
    A = A.astype(int)
    # b value stored in the database is loaded
    ba = np.loadtxt('../Website_database/b.txt')
    ba = ba.astype(float)
    bA = ba.reshape((m,1))
    
    # connects with secure server to obtain secret key and error matrix
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
            eA = conn.recv(1024) 
    
    
    # user chosen password is mapped into a matrix
    P = password_matrix.compute_password_matrix()
    
    # K = value of xor of secret key matrix and password matrix
    K = np.bitwise_xor(data,P) 
    # value of q (field size) for computing the lwe problem.
    q=2**15
    
    # computes the value of b from the given password and compares with existing b value in website_database.
    bA_new = np.matmul(A,K)%q
    bA_new = np.add(bA_new,eA)%q
    

    if (bA==bA_new).all():
        print("Authentication success!!")

    else:
        print("Authentication Failed!!")

    end_time = timeit.default_timer()
    total_time = end_time - start_time 
    print("\nTotal time taken in seconds: ", end_time - start_time)


if __name__ == '__main__':
    compute_b()
    
