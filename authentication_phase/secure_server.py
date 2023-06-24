'''
As per protocols mentioned in the paper, secure server stores creates a secret matrix
and sends it to the website. Website creates error matrix eA computes the value of b and sends
the error matrix back to the secure server.
'''

from mlsocket import MLSocket
import numpy as np
from numpy import random


def send_sA_eA():
    HOST = '127.0.0.1'
    PORT = 65435

    n = 752
    # secret key matrix is loaded from secret_key.txt
    sa = np.loadtxt('../Secure_server_database/secret_key.txt')
    sa = sa.astype(int)
    sA = sa.reshape((n,1))
    # error matrix is loaded from error.txt
    ea = np.loadtxt('../Secure_server_database/error.txt')
    ea = ea.astype(float)
    eA = ea.reshape((n,1))


    # Send data
    with MLSocket() as s:
        # Connect to the port and host
        s.connect((HOST, PORT)) 
        # secret key matrix and error matrix
        s.send(sA)
        s.send(eA) 
    

if __name__ == '__main__':
    send_sA_eA()
    