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
import inv
from operator import matmul


def compute_new_b():
    # Initializes the value of m and n
    n = 192
    m = 192
    l = 80
    q = 8191
    # loads the value of a from website database
    # Matrix A is loaded from A.txt file
    A = np.loadtxt('../Website_database/A.txt') 
    A = A.astype(int)

    # loads the value of matrix b from website database
    b = np.loadtxt('../Website_database/b.txt')
    b = b.astype(float)
    bA = b.reshape((m,l))

    # A connection is established to receive the error matrix and secret key. 
    HOST = '127.0.0.1'
    PORT = 65435

    with MLSocket() as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, address = s.accept()
        
        
        # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
        with conn:
            sA = conn.recv(1024)
            eA = conn.recv(1024) 
    start_time = timeit.default_timer()
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
    np.savetxt('../Website_database/b.txt',b_new)
    end_time = timeit.default_timer()
    total_time = end_time - start_time
    print("Value of b updated!!")
    #print("\nTotal time taken in seconds: ", end_time - start_time)
    # new computed matrix is stored in datbase.
    


if __name__ == '__main__':
    compute_new_b()
