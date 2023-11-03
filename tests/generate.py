from datetime import datetime, timedelta
from random import random, randint
import pandas as pd


from softhouse.config import DATE_FORMAT, PATH_TO_INPUT


def random_input(n_days=10, n_updates_max=10, prob=1.0, stocks=["ABB", "NCC"]):
    """Generates a random input file."""

    # random last and next last prices
    last_prices = dict((code, randint(10, 100)) for code in stocks)
    # last_prices = {"NCC": 10, "ABB": 10, "AddLife B": 10, "SSAB": 10, "8TRA": 10}

    next_last_prices = dict(
        (code, last_prices[code] + randint(3, 10)) 
        for code in stocks
    )
    # next_last_prices = {"NCC": 20, "ABB": 21, "AddLife B": 22, "SSAB": 11, "8TRA": 10}

    # calculated percentages
    percentages = dict(
        (
            code, 
            (last_prices[code] - next_last_prices[code]) \
            / next_last_prices[code]
        ) 
        for code in stocks
    )    

    # calculate winners
    stock_info = [
        dict(name=code, percent=100*percentages[code], 
            latest=last_prices[code]) 
        for code in stocks
    ]
    stock_info = sorted(stock_info, key=(lambda stock: stock["percent"]), 
        reverse=True)
    winners = []
    for i, stock in enumerate(stock_info[0:3]):
        winners.append(dict(
            rank = i + 1,
            name = stock["name"],
            percent = round(stock["percent"], 2), 
            latest = stock["latest"],
        ))
    expected_output = {"winners": winners}

    updates = []
    date = datetime(year=2023, month=10, day=1, hour=12)
    
    # last day, make an update for all stocks
    for code in stocks:
        updates.append(
            [date.strftime(DATE_FORMAT), code, last_prices[code]])
        date -= timedelta(days=0, seconds=randint(0, 5))     

    next_last_updated = set()

    for i in range(n_days):
        date -= timedelta(days=1)  # one day backwards
        n_updates = randint(0, n_updates_max)
        for i in range(n_updates):

            # select a random code
            code = stocks[randint(0, len(stocks)-1)]
            # if next last update has not been made yet for this code
            if not code in next_last_updated: 
                price = next_last_prices[code]
                next_last_updated.add(code)
            else:  # if it has been made, make a random update instead
                price = randint(10, 100)
            updates.append([date.strftime(DATE_FORMAT), code, price])
            date -= timedelta(days=0, seconds=randint(0, 5))

    # put in reverse order in a dataframe                    
    df = pd.DataFrame(updates[::-1])    
    df.to_csv(PATH_TO_INPUT, sep=";", header=["Date", "Kod", "Kurs"], 
        index=False)
    return expected_output