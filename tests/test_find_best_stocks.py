import pytest
from .fixtures import generate_simple_input, simple_output, assert_output_equal

from softhouse.find_best_stocks import find_best_stocks_brute_force


def test_brute_force(generate_simple_input, simple_output):   
    output = find_best_stocks_brute_force(n=3)
    assert_output_equal(output, simple_output)