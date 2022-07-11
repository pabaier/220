from helpers import build_test
from tests.hw8.test_data import *
from tests.test_framework import *


def main():
    builder = TestBuilder("hw 8", 'hw8.py', linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue',
    })
    builder.add_items(build_add_ten_tests(10))
    builder.add_items(build_square_each_tests(10))
    builder.add_items(build_sum_list_tests(10))
    builder.add_items(build_to_numbers_tests(10))
    builder.add_items(build_sum_of_squares_tests(10))
    builder.add_items(build_starter_tests())
    builder.add_items(build_leap_year_tests(10))
    builder.add_items(build_did_overlap_tests(10))
    builder.run()


def build_add_ten_tests(n):
    return build_test('add_ten', add_ten_tests, n)


def build_square_each_tests(n):
    return build_test('square_each', square_each_tests, n)


def build_sum_of_squares_tests(n):
    return build_test('sum_of_squares', sum_of_squares_tests, n)


def build_sum_list_tests(n):
    return build_test('sum_list', sum_list_tests, n)


def build_to_numbers_tests(n):
    return build_test('to_numbers', to_numbers_tests, n)


def build_starter_tests():
    return build_test('starter', starter_tests, 1)


def build_leap_year_tests(n):
    return build_test('leap_year', leap_year_tests, n)


def build_did_overlap_tests(n):
    return build_test('did_overlap', did_overlap_tests, n)
