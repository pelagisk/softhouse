import os
from datetime import datetime, timedelta
from random import random, randint
from math import isclose
import pandas as pd
import pytest

from softhouse.config import PATH_TO_INPUT, DATE_FORMAT
from softhouse.api import update_winners
from softhouse.watch import create_observer


@pytest.fixture()
def generate_zeroline_input(): 
    """Writes twoline input data to file and deletes it afterwards."""   

    test_content = \
"""Date;Kod;Kurs
    """

    with open(PATH_TO_INPUT, "w") as file:
        file.writelines(test_content)
    
    # teardown
    yield 
    os.remove(PATH_TO_INPUT)


@pytest.fixture()
def zeroline_expected_output():  
    """Creates the expected output data in the zeroline case"""
    return {
        "winners": [
        ],
    }


@pytest.fixture()
def generate_twoline_input(): 
    """Writes twoline input data to file and deletes it afterwards."""   

    test_content = \
"""Date;Kod;Kurs
2017-01-01 12:00:00;ABB;217
2017-01-01 12:00:01;NCC;122
    """

    with open(PATH_TO_INPUT, "w") as file:
        file.writelines(test_content)
    
    # teardown
    yield 
    os.remove(PATH_TO_INPUT)


@pytest.fixture()
def twoline_expected_output():  
    """Creates the expected output data in the twoline case"""
    return {
        "winners": [
            {"rank": 1, "name": "ABB", "percent": 0, "latest": 217}, 
            {"rank": 2, "name": "NCC", "percent": 0, "latest": 122}, 
        ],
    } 


@pytest.fixture()
def generate_multiline_input(): 
    """Writes multiline input data to file and deletes it afterwards."""   

    test_content = \
"""Date;Kod;Kurs
2017-01-01 12:00:00;ABB;217
2017-01-01 12:00:01;NCC;122
2017-01-01 12:00:02;ABB;218
2017-01-01 12:00:03;NCC;123
2017-01-01 12:00:04;NCC;121
2017-01-01 12:00:05;AddLife B;21
2017-01-01 12:00:06;NCC;121
2017-01-01 12:00:06;SSAB B;221
2017-01-01 12:01:04;8TRA;226
2017-01-01 12:01:05;AddLife B;27
2017-01-01 12:01:06;NCC;119
2017-01-01 12:01:07;ABB;219
2017-01-02 12:00:07;ABB;222
2017-01-02 12:00:08;NCC;117
2017-01-02 12:00:09;NCC;116
2017-01-02 12:00:10;8TRA;225
2017-01-02 12:00:23;SSAB B;209
2017-01-02 12:01:10;AddLife B;38
2017-01-02 12:01:09;NCC;116
2017-01-02 12:02:09;NCC;118
2017-01-02 12:03:09;NCC;121
    """

    with open(PATH_TO_INPUT, "w") as file:
        file.writelines(test_content)
    
    # teardown
    yield 
    os.remove(PATH_TO_INPUT)


@pytest.fixture()
def multiline_expected_output():  
    """Creates the expected output data in the multiline case"""
    return {
        "winners": [
            {"rank": 1, "name": "AddLife B", "percent": 40.74, "latest": 38}, 
            {"rank": 2, "name": "NCC", "percent": 1.68, "latest": 121}, 
            {"rank": 3, "name": "ABB", "percent": 1.37, "latest": 222},
        ],
    } 


def assert_output_equal(actual, expected, rel_tol=1e-9):
    """Asserts that the output dict "actual" is equal to "expected" up to rel_tol."""
    assert(actual.keys() == expected.keys())    
    for test_stock, expected_stock in zip(actual["winners"], expected["winners"]):        
        assert(test_stock.keys() == expected_stock.keys())
        for key in ["rank", "name"]:
            assert(test_stock[key] == expected_stock[key])
        # float almost-equality
        assert(isclose(test_stock["percent"], expected_stock["percent"], rel_tol=rel_tol))


@pytest.fixture()
def setup_api():
    """Sets up the API for testing since the lifespan function does not work in this case."""
    update_winners()
    observer = create_observer(PATH_TO_INPUT, lambda event: update_winners())
    yield
    observer.stop()


@pytest.fixture()
def generate_random_input():
    """Writes random input data to file and deletes it afterwards.    
    """   

    # stock codes
    codes = ["NCC", "ABB", "AddLife B", "SSAB", "8TRA"]

    # random last and next last prices
    last_prices = dict((code, randint(10, 100)) for code in codes)
    next_last_prices = dict((code, randint(10, 100)) for code in codes)

    # calculated percentages
    percentages = dict(
        (code, (last_prices[code] - next_last_prices[code]) / next_last_prices[code]) 
        for code in codes
    )

    # calculate winners
    stock_info = [
        dict(name=code, percent=100*percentages[code], latest=last_prices[code]) 
        for code in codes
    ]
    stock_info = sorted(stock_info, key=(lambda stock: stock["percent"]), reverse=True)
    winners = []
    for i, stock in enumerate(stock_info[0:3]):
        winners.append(dict(
            rank = i + 1,
            name = stock["name"],
            percent = round(stock["percent"], 2), 
            latest = stock["latest"],
        ))
    expected_output = {"winners": winners}

    def _method(n_days=10, n_updates_max=10, prob=1.0):
        updates = []
        date = datetime(year=2023, month=10, day=1, hour=12)
        
        # last day, make an update for all stocks
        for code in codes:
            updates.append([date.strftime(DATE_FORMAT), code, last_prices[code]])
            date -= timedelta(days=0, seconds=randint(0, 5))     

        next_last_updated = set()

        for i in range(n_days):
            date -= timedelta(days=1)  # one day backwards
            n_updates = randint(0, n_updates_max)
            for i in range(n_updates):
                # TODO ensure that code appears at least once
                # select a random code
                code = codes[randint(0, len(codes)-1)]
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
        df.to_csv(PATH_TO_INPUT, sep=";", header=["Date", "Kod", "Kurs"], index=False)
        return expected_output

    yield _method
    os.remove(PATH_TO_INPUT)