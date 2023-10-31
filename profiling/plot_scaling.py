import os
from timeit import timeit
import matplotlib.pyplot as plt

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_brute_force
from softhouse.winners import find_winners_alternative

from profiling.generate import generate_input


# check scaling of resources with input size
iterations = 100
n_list = [2**n for n in range(2, 8)]

pandas_elapsed_list = []
alternative_elapsed_list = []

n_rows_list = []
for n in n_list:
    n_rows = generate_input(n_days=n)
    n_rows_list.append(n_rows)

    t = timeit("find_winners_brute_force(PATH_TO_INPUT)", number=iterations, globals=globals())
    pandas_elapsed_list.append(t)

    t = timeit("find_winners_alternative(PATH_TO_INPUT)", number=iterations, globals=globals())
    alternative_elapsed_list.append(t)
    
# delete input file
os.remove(PATH_TO_INPUT)

# plot results
fig, ax = plt.subplots()
ax.plot(n_rows_list, pandas_elapsed_list, ".-b", label="Pandas")
ax.plot(n_rows_list, alternative_elapsed_list, ".-r", label="Alternative")
ax.set_xlabel("File size")
ax.set_ylabel("Time in seconds")
ax.legend()
plt.show()

# clearly, the running time increases linearly with the file size