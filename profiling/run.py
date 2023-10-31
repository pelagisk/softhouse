import os
from cProfile import Profile
from pstats import SortKey, Stats

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_brute_force

from profiling.generate import generate_input


# prepare profiling by generating a large input file
generate_input(n_days=500)

with Profile() as profile:

    find_winners_brute_force(PATH_TO_INPUT)
    (
        Stats(profile)
        .sort_stats(SortKey.TIME)
        .print_stats()
    )

# delete input file
# os.remove(PATH_TO_INPUT)