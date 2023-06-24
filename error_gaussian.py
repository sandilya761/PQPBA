from numpy import random
import numpy as np

x = random.normal(size = (7,1))
#y = random.normal(loc = 1, scale = 2, size = (7,1))

q = 2**15
# Set the desired range for the normal distribution
lower_bound = -q/4
upper_bound = q/4

# Set the mean and standard deviation of the normal distribution
mean = 0
std_dev = 1
m = 752
# Generate random numbers from the normal distribution
random_numbers = np.random.normal(mean, std_dev, size=(m,1))

# Truncate the random numbers to the desired range
random_numbers = np.clip(random_numbers, lower_bound, upper_bound)

# Print the generated random numbers
print(random_numbers)



#print(x)
