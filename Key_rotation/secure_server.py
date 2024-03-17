'''
This file creates a new secret key matrix new_sA and replaces the old_sA from the database (sA.txt file).
Once new_sA is created, it is xored with old_sA matrix and sends the value to the website. Website uses
the received value and updates the lwe instance values (bA matrix). 

'''
import numpy as np
import sys
from numpy import random
from mlsocket import MLSocket

# creates a new secret key new_sA
m = 192
n = 192
l = 80
q = 8191
new_sA = np.random.randint(0,(q)-1,size = (n,l))



def gen_new_key():
    HOST = '127.0.0.1'
    PORT = 65435

    # Load the array from the text file (database which contains the secret key)
    old_sa = np.loadtxt('../Secure_server_database/secret_key.txt')

    # converts the elements of np array from float to int 
    old_sa = old_sa.astype(int)
       
    # XORs the old_sA value with new_sA value 
    old_sA = old_sa.reshape((n,l))
    sA = np.bitwise_xor(old_sA,new_sA)

    # loads the error matrix from error.txt file
    ea = np.loadtxt('../Secure_server_database/error.txt')
    ea = ea.astype(float)
    eA = ea.reshape((m,l))
    
    # sends the sA value and eA to the website

    with MLSocket() as s:
        s.connect((HOST, PORT)) # Connect to the port and host
        s.send(sA) # After sending the secret key matrix
        s.send(eA) # sends the error matrix



# deletes the old_sA value in the database and updates it with new_sA value.
def update_database():

    #Save the array to a text file

    np.savetxt('../Secure_server_database/secret_key.txt', new_sA)




if __name__ == '__main__':

    gen_new_key()
    
    update_database()
