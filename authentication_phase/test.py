import numpy as np
from numpy import random

m = 4
b = np.random.randint(0,2500,size = (m,1))
b_new = np.random.randint(0,2500,size = (m,1))

print(b)
print(b_new)

if (b == b).all():
    print("true")
else:
    print("false")    
