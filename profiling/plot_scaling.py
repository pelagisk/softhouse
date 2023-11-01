import os
from timeit import timeit
import numpy as np
import matplotlib.pyplot as plt

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_pandas
from softhouse.winners import find_winners_alternative

from profiling.generate import generate_input


"""
Uses timeit and averaging over several generated input files to investigate the 
scaling of the two methods: pandas or alternative
"""


# probability of a daily update 
prob = 0.8

# check scaling of resources with input size
timeit_iterations = 10
avg_iterations = 100

n_list = [2**n for n in range(4, 10)]

n_avg_list = []
pandas_avg_list = []
pandas_std_list = []
alternative_avg_list = []
alternative_std_list = []

for n in n_list:

    # take the average over several generated input files
    nrl = []
    pel = []
    ael = []    
    for i in range(avg_iterations):        
        n_rows = generate_input(n_days=n, prob=prob)
        # take the average over several runs
        tp = timeit("find_winners_pandas(PATH_TO_INPUT)", number=timeit_iterations, globals=globals())
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