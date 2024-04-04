'''This file is used to calculate inverse modulo matrix. This code is taken
from https://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
'''

import numpy as np
from ctypes import sizeof
from operator import matmul
import password_matrix

def generalizedEuclidianAlgorithm(a, b):
    if b > a:
        return generalizedEuclidianAlgorithm(b,a)
    elif b == 0:
        return (1, 0)
    else:
        (x, y) = generalizedEuclidianAlgorithm(b, a % b)
        return (y, x - (a // b) * y)

def inversemodp(a, p):
    a = a % p
    if (a == 0):
        print ("a is 0 mod p")
        return None
    if a > 1 and p % a == 0:
        return None
    (x,y) = generalizedEuclidianAlgorithm(p, a % p)
    inv = y % p
    #assert (inv * a) % p == 1
    return inv

def identitymatrix(n):
    return [[int(x == y) for x in range(0, n)] for y in range(0, n)]


def inversematrix(matrix, q):
    n = len(matrix)
    A = np.matrix([[ matrix[j, i] for i in range(0,n)] for j in range(0, n)], dtype = int)
    Ainv = np.matrix(identitymatrix(n), dtype = int)
    for i in range(0, n):
        factor = inversemodp(A[i,i], q)
        #print(factor)
        #if factor is None:
        #     raise ValueError("TODO: deal with this case")
        A[i] = A[i] * factor % q
        Ainv[i] = Ainv[i] * factor % q
        for j in range(0, n):
            if (i != j):
                factor = A[j, i]
                A[j] = (A[j] - factor * A[i]) % q
                Ainv[j] = (Ainv[j] - factor * Ainv[i]) % q
    return Ainv

