import os
from timeit import timeit
import matplotlib.pyplot as plt

import logging
from softhouse.config import PATH_TO_INPUT, LOG_FILENAME
from softhouse.winners import find_winners_pandas
from softhouse.winners import find_winners_alternative

from profiling.generate import generate_input


logging.basicConfig(
    filename=LOG_FILENAME, 
    level=logging.DEBUG,
    filemode='w', 
    format='%(message)s'
)

n = 100
n_rows = generate_input(n_days=n, prob=0.8)
print(f"n_rows: {n_rows}")

res = find_winners_alternative(PATH_TO_INPUT)
print(res["winners"])

# with open(LOG_FILENAME) as f:
#     print(f.read())
    

# delete input file
os.remove(PATH_TO_INPUT)