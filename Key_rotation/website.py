'''
Website receives the xor of the old_sA and new_sA. It computes the new lwe instance as mentioned in protocol3.
Please refer to protcol3 in the paper for more details.
'''
from mlsocket import MLSocket
import numpy as np
import sys
from numpy import random
import timeit
import password_matrix

# Initializes the value of m and n
n = 752

def compute_new_b():
    # loads the value of a from the database
    # Matrix A is loaded from A.txt file
    A = np.loadtxt('../Website_database/A.txt') 
    A = A.astype(int)

    # A connection is established to receive the error matrix and secret key. 
    HOST = '127.0.0.1'
    PORT = 65435

    with MLSocket() as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, address = s.accept()
        start_time = timeit.default_timer()
        
        # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
        with conn:
            sA = conn.recv(1024)
            error = conn.recv(1024) 
    
    
    # user chosen password is mapped into a matrix
    P = password_matrix.compute_password_matrix()

    # K = value of xor of secret key matrix and password matrix
    
    K = np.bitwise_xor(sA,P) 
     
    
    # value of q (field size) for computing the lwe problem.
    q= 2**15

    # value of b is computed
    bA = np.matmul(A,K)%q
    bA = np.add(bA,error)%q
    end_time = timeit.default_timer()
    total_time = end_time - start_time
    print("Value of b updated!!")
    print("\nTotal time taken in seconds: ", end_time - start_time)
    # new computed matrix is stored in datbase.
    np.savetxt('../Website_database/b.txt',bA)


if __name__ == '__main__':
    compute_new_b()
