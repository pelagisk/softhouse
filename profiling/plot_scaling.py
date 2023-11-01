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
scaling of the two methods: pandas or alternative.
"""

timeit_iterations = 10
avg_iterations = 100

fig, ax = plt.subplots()

n_list = [2**n for n in range(4, 10)]

n_avg = np.zeros(len(n_list))
pandas_avg = np.zeros(len(n_list))
pandas_std = np.zeros(len(n_list)) 
alternative_avg = np.zeros(len(n_list))
alternative_std = np.zeros(len(n_list)) 
alternative2_avg = np.zeros(len(n_list))
alternative2_std = np.zeros(len(n_list)) 

for (i, n) in enumerate(n_list):

    # take the average over several generated input files
    ns = np.zeros(avg_iterations)
    pts = np.zeros(avg_iterations)
    ats = np.zeros(avg_iterations)
    a2ts = np.zeros(avg_iterations)

    for j in range(avg_iterations):        
        ns[j] = generate_input(n_days=n, prob=1.0)
        # take the average over several runs
        pts[j] = timeit("find_winners_pandas(PATH_TO_INPUT)", 
            number=timeit_iterations, globals=globals())
        ats[j] = timeit(
            "find_winners_alternative(PATH_TO_INPUT, assume_update_every_day=False)", 
            number=timeit_iterations, globals=globals())                
        a2ts[j] = timeit(
            "find_winners_alternative(PATH_TO_INPUT, assume_update_every_day=True)", 
            number=timeit_iterations, globals=globals()) 
    
    n_avg[i] = np.average(ns)
    pandas_avg[i] = np.average(pts)
    pandas_std[i] = np.std(pts)
    alternative_avg[i] = np.average(ats)
    alternative_std[i] = np.std(ats)
    alternative2_avg[i] = np.average(a2ts)
    alternative2_std[i] = np.std(a2ts)
    
# delete input file
os.remove(PATH_TO_INPUT)

# plot results
ax.errorbar(n_avg, pandas_avg, yerr=pandas_std, 
    fmt=".-", label=f"Pandas")
ax.errorbar(n_avg, alternative_avg, yerr=alternative_std, 
    fmt=".-", label=f"Alternative")
ax.errorbar(n_avg, alternative2_avg, yerr=alternative2_std, 
    fmt=".-", label=f"Alternative, assuming updates every day")

ax.set_xlabel("Average number of lines in input file")
ax.set_ylabel("Average runtime in seconds")
ax.legend()
fig.savefig("profiling/scaling.png")
plt.show()