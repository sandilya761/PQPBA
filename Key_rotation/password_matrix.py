'''
password_matrix.py file salts the password and convert into its hashed form.
Hashed passsword is converted into a matrix of required dimension (m x 1). 
The size of salt and number of iterations are selected as per NIST standard. 
Please refer to NIST Special Publication 800-132 (https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf) 
for more details.
'''
import hashlib
import numpy as np
from hashlib import pbkdf2_hmac
import os

def compute_password_matrix():
    m = 752
    iters = 1000
    ''' first parameter is the hashing algortihm type and second parameteris the password string, third is the 
    salt string and last one is iterations
    '''
    salt = b'saltsalt'
    password = b'password'
    dk = pbkdf2_hmac('sha512', password, salt, iters)

    password_hex = dk.hex()
    password_int = int(password_hex,16)
    s = str(int(password_hex,16))
    # password string is appended with 0s until the length of the string is equal to m value 
    while(len(s)!=752):
        s = s + '0'

    pwd = np.array(list(s), dtype=int)
    # reshaps the matrix to m X 1 dimension
    pwd_matrix = pwd.reshape((m,1))
    
    return pwd_matrix
        



