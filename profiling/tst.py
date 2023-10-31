import os
from timeit import timeit
import matplotlib.pyplot as plt

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_brute_force
from softhouse.winners import find_winners_alternative

from profiling.generate import generate_input


# check scaling of resources with input size
iterations = 100

n_rows = generate_input(n_days=100)

find_winners_alternative(PATH_TO_INPUT)

# t = timeit("find_winners_brute_force(PATH_TO_INPUT)", number=iterations, globals=globals())
# print("Pandas: {t:.%f} s")

# t = timeit("find_winners_alternative(PATH_TO_INPUT)", number=iterations, globals=globals())
# print("Alternative: {t:.%f} s")