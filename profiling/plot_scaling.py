import os
from timeit import timeit
import numpy as np
import matplotlib.pyplot as plt

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_brute_force
from softhouse.winners import find_winners_alternative

from profiling.generate import generate_input


# probability of a daily update 
prob = 1.0

# check scaling of resources with input size
timeit_iterations = 10
avg_iterations = 100

# n_list = [50 * n for n in range(1, 5)]
n_list = [50, 100, 150, 200]

# n_list = [2**n for n in range(4, 6)]

n_avg_list = []
pandas_avg_list = []
pandas_std_list = []
alternative_avg_list = []
alternative_std_list = []

for n in n_list:

    print(f"n = {n}")

    # take the average over several generated input files
    nrl = []
    pel = []
    ael = []
    for i in range(avg_iterations):        
        n_rows = generate_input(n_days=n, prob=prob)
        print(f"    n_rows = {n_rows}")
        # take the average over several runs
        tp = timeit("find_winners_brute_force(PATH_TO_INPUT)", number=timeit_iterations, globals=globals())
        ta = timeit("find_winners_alternative(PATH_TO_INPUT)", number=timeit_iterations, globals=globals())                
        nrl.append(n_rows)
        pel.append(tp)
        ael.append(ta)
    
    n_avg_list.append(np.average(nrl))
    pandas_avg_list.append(np.average(pel))
    pandas_std_list.append(np.std(pel))
    alternative_avg_list.append(np.average(ael))
    alternative_std_list.append(np.std(ael))
    
# delete input file
os.remove(PATH_TO_INPUT)

# plot results
fig, ax = plt.subplots()
ax.errorbar(n_avg_list, pandas_avg_list, yerr=pandas_std_list, fmt=".-b", label="Pandas")
ax.errorbar(n_avg_list, alternative_avg_list, yerr=pandas_std_list, fmt=".-r", label="Alternative")
ax.set_xlabel("File size")
ax.set_ylabel("Time in seconds")
ax.legend()
plt.show()