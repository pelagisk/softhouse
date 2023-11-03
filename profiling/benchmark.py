import os
from timeit import timeit
import numpy as np
import matplotlib.pyplot as plt

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_pandas
from softhouse.winners import find_winners_python

from profiling.generate import generate_input


"""
Uses timeit and averaging over several generated input files to benchmark the 
scaling of the two methods: pandas or python.
"""

timeit_iterations = 10
avg_iterations = 100

fig, ax = plt.subplots()

n_list = [2**n for n in range(4, 10)]

n_avg = np.zeros(len(n_list))
pandas_avg = np.zeros(len(n_list))
pandas_std = np.zeros(len(n_list)) 
python_avg = np.zeros(len(n_list))
python_std = np.zeros(len(n_list)) 
python_stocks_avg = np.zeros(len(n_list))
python_stocks_std = np.zeros(len(n_list)) 

for (i, n) in enumerate(n_list):

    # take the average over several generated input files
    ns = np.zeros(avg_iterations)
    pd_ts = np.zeros(avg_iterations)
    py_ts = np.zeros(avg_iterations)
    pa_ts = np.zeros(avg_iterations)

    for j in range(avg_iterations):        
        ns[j] = generate_input(n_days=n, prob=1.0)
        # take the average over several runs
        pd_ts[j] = timeit("find_winners_pandas(PATH_TO_INPUT)", 
            number=timeit_iterations, globals=globals())
        py_ts[j] = timeit(
            "find_winners_python(PATH_TO_INPUT)", 
            number=timeit_iterations, globals=globals())                
        pa_ts[j] = timeit(
            (
                "find_winners_python(PATH_TO_INPUT, "
                "stocks=['NCC', 'ABB', 'AddLife B', '8TRA', 'SSAB'])"
            ), 
            number=timeit_iterations, globals=globals()) 
    
    n_avg[i] = np.average(ns)
    pandas_avg[i] = np.average(pd_ts)
    pandas_std[i] = np.std(pd_ts)
    python_avg[i] = np.average(py_ts)
    python_std[i] = np.std(py_ts)
    python_stocks_avg[i] = np.average(pa_ts)
    python_stocks_std[i] = np.std(pa_ts)
    
# delete input file
os.remove(PATH_TO_INPUT)

# plot results
ax.errorbar(n_avg, pandas_avg, yerr=pandas_std, 
    fmt=".-", label=f"Pandas")
ax.errorbar(n_avg, python_avg, yerr=python_std, 
    fmt=".-", label=f"Alternative")
ax.errorbar(n_avg, python_stocks_avg, yerr=python_stocks_std, 
    fmt=".-", label=f"Alternative, assuming the list of stocks is known")

ax.set_xlabel("Average number of lines in input file")
ax.set_ylabel("Average runtime in seconds")
ax.legend()
fig.savefig("profiling/scaling.png")
plt.show()