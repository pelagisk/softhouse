import os
from math import isclose
import pytest

from tests.generate import random_input

from softhouse.config import PATH_TO_INPUT, DATE_FORMAT
from softhouse.api import update_winners
from softhouse.watch import create_observer
from softhouse.winners import find_winners_pandas, find_winners_python


@pytest.fixture()
def n():
    return 3


@pytest.fixture()
def setup_input_file():

    def _method(input_string):
        with open(PATH_TO_INPUT, "w") as file:
            file.writelines(input_string)
    
    yield _method

    os.remove(PATH_TO_INPUT)


@pytest.fixture()
def zeroline_io():
    input_str = "Date;Kod;Kurs\n"
    winners = []
    return input_str, {"winners": winners}


@pytest.fixture()
def twoline_io():
    input_str = """Date;Kod;Kurs
2017-01-01 12:00:00;ABB;217
2017-01-01 12:00:01;NCC;122"""
    winners = [
        {"rank": 1, "name": "ABB", "percent": 0, "latest": 217}, 
        {"rank": 2, "name": "NCC", "percent": 0, "latest": 122}, 
    ]
    return input_str, {"winners": winners}


@pytest.fixture()
def multiline_io(): 
    input_str = """Date;Kod;Kurs
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
2017-01-02 12:03:09;NCC;121"""
    winners = [
        {"rank": 1, "name": "AddLife B", "percent": 40.74, "latest": 38}, 
        {"rank": 2, "name": "NCC", "percent": 1.68, "latest": 121}, 
        {"rank": 3, "name": "ABB", "percent": 1.37, "latest": 222},
    ]
    return input_str, {"winners": winners}


@pytest.fixture()
def stocks():
    return ["NCC", "ABB", "AddLife B", "8TRA", "SSAB"]


@pytest.fixture()
def setup_api():
    """
    Sets up the API for testing since the lifespan function does not work in 
    this case.
    """
    update_winners()
    observer = create_observer(PATH_TO_INPUT, lambda event: update_winners())
    yield
    observer.stop()


@pytest.fixture()
def n_days():
    return 40


@pytest.fixture()
def n_updates_max():
    return 30


@pytest.fixture()
def prob():
    return 1.0


@pytest.fixture()
def generate_random_input(stocks, n_days, n_updates_max, prob):
    """Writes random input data to file and deletes it afterwards.    
    """   

    def _method():
        return random_input(
            stocks=stocks, 
            n_days=n_days, 
            n_updates_max=n_updates_max, 
            prob=prob
        )

    yield _method
    os.remove(PATH_TO_INPUT)


def find_equivalences(enum, key):
    classes = dict()
    for e in enum:
        k = key(e)
        if not k in classes:
            classes[k] = []
        classes[k].append(e)
    return list(classes.values())


def assert_output_equal(actual_output, expected_output, rel_tol=1e-9):
    """
    Asserts that the output dict "actual" is equal to "expected" up to rel_tol.
    """
    assert(actual_output.keys() == expected_output.keys())    
    actual = actual_output["winners"]
    expected = expected_output["winners"]
    assert(len(actual) == len(expected))

    # divide into equivalence classes, since there may be entries with the same
    # percentage. Each class has the same percentage.
    get_percentage = lambda x: x["percent"]
    actual_eq = find_equivalences(actual, key=get_percentage)
    expected_eq = find_equivalences(expected, key=get_percentage)
    assert(len(actual_eq) == len(expected_eq))
    for aeq, eeq in zip(actual_eq, expected_eq):
        # since dicts are not hashable and due to float equality, we have to test
        # that we can find a corresponding element for each element
        counterparts = []
        for member in aeq:
            has_counterpart = False
            for m in eeq:
                if (
                    (member["name"] == m["name"]) and 
                    isclose(member["percent"], m["percent"], rel_tol=rel_tol)
                ):
                    has_counterpart = True
                    break
            assert(has_counterpart == True)            

    # for stock, expected_stock in zip(actual["winners"], expected["winners"]):        
    #     assert(stock.keys() == expected_stock.keys())
    #     for key in ["rank", "name"]:
    #         assert(stock[key] == expected_stock[key])
    #     # float almost-equality
    #     assert(isclose(stock["percent"], expected_stock["percent"], 
    #         rel_tol=rel_tol))


@pytest.fixture()
def n_attempts():
    return 10