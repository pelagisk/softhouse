import pytest
from .fixtures import *

from softhouse.config import PATH_TO_INPUT


# tests of the pandas algorithm


def test_winners_pandas_zeroline(n, zeroline_io, setup_input_file):
    input_str, expected = zeroline_io
    setup_input_file(input_str)
    output = find_winners_pandas(PATH_TO_INPUT, n=n)
    assert_output_equal(output, expected)  


def test_winners_pandas_twoline(n, twoline_io, setup_input_file):
    input_str, expected = twoline_io
    setup_input_file(input_str)
    output = find_winners_pandas(PATH_TO_INPUT, n=n)
    assert_output_equal(output, expected)  


def test_winners_pandas_multiline(n, multiline_io, setup_input_file):
    input_str, expected = multiline_io
    setup_input_file(input_str)
    output = find_winners_pandas(PATH_TO_INPUT, n=n)
    assert_output_equal(output, expected)  


def test_winners_pandas_random(n, generate_random_input, n_attempts):
    for i in range(n_attempts):
        expected = generate_random_input()
        output = find_winners_pandas(PATH_TO_INPUT, n=n)
        assert_output_equal(output, expected)


# tests of the python algorithm


def test_winners_python_zeroline(n, zeroline_io, setup_input_file):
    input_str, expected = zeroline_io
    setup_input_file(input_str)
    output = find_winners_python(PATH_TO_INPUT, n=n)
    assert_output_equal(output, expected)  


def test_winners_python_twoline(n, twoline_io, setup_input_file):
    input_str, expected = twoline_io
    setup_input_file(input_str)
    output = find_winners_python(PATH_TO_INPUT, n=n)
    assert_output_equal(output, expected)  


def test_winners_python_multiline(n, multiline_io, setup_input_file):
    input_str, expected = multiline_io
    setup_input_file(input_str)
    output = find_winners_python(PATH_TO_INPUT, n=n)
    assert_output_equal(output, expected)  


def test_winners_python_random(n, generate_random_input, n_attempts):
    for i in range(n_attempts):
        expected = generate_random_input()
        output = find_winners_python(PATH_TO_INPUT, n=n)
        assert_output_equal(output, expected)


# assuming knowledge of the list of stocks:


def test_winners_python_stocks_zeroline(n, zeroline_io, setup_input_file, stocks):
    input_str, expected = zeroline_io
    setup_input_file(input_str)
    output = find_winners_python(PATH_TO_INPUT, n=n, stocks=stocks)
    assert_output_equal(output, expected)  


def test_winners_python_stocks_twoline(n, twoline_io, setup_input_file, stocks):
    input_str, expected = twoline_io
    setup_input_file(input_str)
    output = find_winners_python(PATH_TO_INPUT, n=n, stocks=stocks)
    assert_output_equal(output, expected)  


def test_winners_python_stocks_multiline(n, multiline_io, setup_input_file, stocks):
    input_str, expected = multiline_io
    setup_input_file(input_str)
    output = find_winners_python(PATH_TO_INPUT, n=n, stocks=stocks)
    assert_output_equal(output, expected)  


def test_winners_python_stocks_random(n, generate_random_input, n_attempts, stocks):
    for i in range(n_attempts):
        expected = generate_random_input()
        output = find_winners_python(PATH_TO_INPUT, n=n, stocks=stocks)
        assert_output_equal(output, expected)