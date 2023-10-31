from datetime import datetime, timedelta
import pandas as pd
from random import random

from softhouse.config import PATH_TO_INPUT, DATE_FORMAT
from softhouse.winners import find_winners_brute_force


def generate_input(n_days=100, prob=0.8, stocks=["NCC", "ABB", "AddLife B", "SSAB", "8TRA"]):
    """
    Generates an mock input file with random updates of stock price.
    """
    updates = []
    date = datetime(year=2023, month=10, day=1)
    for day_index in range(n_days):
        for code in stocks:
            # with probability prob, update the price
            if random() < prob:                      
                price = int(10 + 1000 * random())
                updates.append([date.strftime(DATE_FORMAT), code, price])
                date += timedelta(days=day_index, seconds=(60 * random()))              
    df = pd.DataFrame(updates)    
    df.to_csv(PATH_TO_INPUT, sep=";", header=["Date", "Kod", "Kurs"], index=False)
    return len(updates)
