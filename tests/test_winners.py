import pytest
from .fixtures import *

from softhouse.config import PATH_TO_INPUT
from softhouse.winners import find_winners_pandas, find_winners_alternative


def test_pandas_zeroline(generate_zeroline_input, zeroline_expected_output):   
    """Tests the brute force algorithm for finding the best stocks."""
    output = find_winners_pandas(PATH_TO_INPUT, n=3)
    assert_output_equal(output, zeroline_expected_output)

def test_pandas_twoline(generate_twoline_input, twoline_expected_output):   
    """Tests the brute force algorithm for finding the best stocks."""
    output = find_winners_pandas(PATH_TO_INPUT, n=3)
    assert_output_equal(output, twoline_expected_output)

def test_pandas_multiline(generate_multiline_input, multiline_expected_output):   
    """Tests the brute force algorithm for finding the best stocks."""
    output = find_winners_pandas(PATH_TO_INPUT, n=3)
    assert_output_equal(output, multiline_expected_output)

def test_pandas_random(generate_random_input):   
    """Tests the brute force algorithm for finding the best stocks."""
    for i in range(10):
        expected_output = generate_random_input(n_days=40, n_updates_max=30)
        output = find_winners_pandas(PATH_TO_INPUT, n=3)
        assert_output_equal(output, expected_output)

def test_alternative_zeroline(generate_zeroline_input, zeroline_expected_output):   
    """Tests the brute force algorithm for finding the best stocks."""
    output = find_winners_alternative(PATH_TO_INPUT, n=3)
    assert_output_equal(output, zeroline_expected_output)

def test_alternative_twoline(generate_twoline_input, twoline_expected_output):   
    """Tests the brute force algorithm for finding the best stocks."""
    output = find_winners_alternative(PATH_TO_INPUT, n=3)
    assert_output_equal(output, twoline_expected_output)

def test_alternative_multiline(generate_multiline_input, multiline_expected_output):   
    """Tests the brute force algorithm for finding the best stocks."""
    output = find_winners_alternative(PATH_TO_INPUT, n=3)
    assert_output_equal(output, multiline_expected_output)

def test_alternative_random(generate_random_input):   
    """Tests the brute force algorithm for finding the best stocks."""
    for i in range(10):
        expected_output = generate_random_input(n_days=40, n_updates_max=30)
        output = find_winners_alternative(PATH_TO_INPUT, n=3)
        assert_output_equal(output, expected_output)