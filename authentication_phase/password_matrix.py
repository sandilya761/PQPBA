'''
password_matrix.py file salts the password and convert into its hashed form.
Hashed passsword is converted into a matrix of required dimension (n x l). 
'''
import hashlib
import numpy as np
from hashlib import pbkdf2_hmac
import os

def compute_password_matrix():
    m = 192
    n = 192
    l = 80
    
    ''' first parameter is the hashing algortihm type and second parameteris the password string, third is the 
    salt string and last one is iterations
    '''
    h = 'password'
    h_digest = hashlib.shake_256(h.encode('UTF-8'))

    i = 6378
    password_hex = h_digest.hexdigest(i)
    #print(password_hex)

    password_int = int(password_hex,16)
    s = str(int(password_hex,16))
    #s = s+'0'
    pwd = np.array(list(s), dtype=int)
    # reshaps the matrix to n X l dimension
    pwd_matrix = pwd.reshape((192,80))
    return pwd_matrix    
    



