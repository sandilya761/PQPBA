import numpy as np
from numpy import random

x = np.random.randint(0,2500,size = (4,1)) # secret key matrix is generated
print(type(x))
np.savetxt('test/x.txt',x)
