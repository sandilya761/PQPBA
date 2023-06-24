import numpy as np

m = 752
n = 752

# Create a NumPy array
A = np.random.randint(0,(2**15)-1,size = (m,n)) # secret key matrix is generated

# Save the array to a text file
np.savetxt('A.txt', A)


# Load the array from the text file
my_array = np.loadtxt('A.txt')
print(my_array)

'''print(sA_new)

sA_new_1 = np.random.randint(0,2500,size = (4,1)) # secret key matrix is generated

new_key = np.bitwise_xor(sA_new,sA_new_1)
print(new_key)
'''
