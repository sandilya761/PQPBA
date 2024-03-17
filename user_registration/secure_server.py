'''
As per protocols mentioned in the paper, secure server stores creates a secret matrix
and sends it to the website. Website creates error matrix eA computes the value of b and sends
the error matrix back to the secure server.
'''

from mlsocket import MLSocket
import numpy as np
from numpy import random


def send_sA():
    HOST = '127.0.0.1'
    PORT = 65435
    n = 192
    l = 80
    q = 8191
    # secret key matrix is generated
    sA = np.random.randint(0,q-1,size = (n,l)) 
    # Send data
    with MLSocket() as s:
        # Connect to the port and host
        s.connect((HOST, PORT)) 
        # After sending the secret key matrix
        s.send(sA) 
    #store the matrix sA in its database sA.txt
    np.savetxt('../Secure_server_database/secret_key.txt',sA)


def receive_error():
    HOST = '127.0.0.1'
    PORT = 65530
    with MLSocket() as e:
        e.bind((HOST, PORT))
        e.listen()
        conn, address = e.accept()
        # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
        with conn:
            eA = conn.recv(1024) 
    
    
    # store the received error matrix in error.txt

    np.savetxt('../Secure_server_database/error.txt',eA)


if __name__ == '__main__':
    send_sA()
    receive_error()