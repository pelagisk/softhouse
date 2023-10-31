import os
from timeit import timeit
import matplotlib.pyplot as plt

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_brute_force

from profiling.generate import generate_input


# check scaling of resources with input size
iterations = 100
n_values = [2**n for n in range(2, 10)]

time_values = []
n_rows_values = []
for n in n_values:
    n_rows = generate_input(n_days=n)
    t = timeit("find_winners_brute_force(PATH_TO_INPUT)", number=iterations, globals=globals())

    n_rows_values.append(n_rows)
    time_values.append(t)
    
    
# delete input file
os.remove(PATH_TO_INPUT)

# plot results
fig, ax = plt.subplots()
ax.plot(n_rows_values, time_values, ".-")
ax.set_xlabel("File size")
ax.set_ylabel("Time in seconds")
plt.show()

# clearly, the running time increases linearly with the file size