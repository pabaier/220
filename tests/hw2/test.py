import os
from pathlib import Path

from tests import test_framework as t
from tests.hw2.test_data import *

test_file = Path(os.path.dirname(hw2.__file__)) / 'hw2.py'


def main():
    builder = t.TestBuilder("hw 2", test_file, linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'if (?!__name__).*:': 'if statements not allowed for this assignment. please remove it to continue',
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue',
        '\[*\]': 'lists are not allowed for this assignment. please remove it to continue',
        'list': 'lists are not allowed for this assignment. please remove it to continue',
        'pow.*\(.*\d\)': 'cannot use pow function for this assignment!',
        '\*\*': 'cannot use exponent operator for this assignment!',
        '\".*\+': 'string concatenation not allowed for this assignment. please remove it to continue',
        '\+.*\"': 'string concatenation not allowed for this assignment. please remove it to continue',
        '\'.*\+': 'string concatenation not allowed for this assignment. please remove it to continue',
        '\+.*\'': 'string concatenation not allowed for this assignment. please remove it to continue'

    })

    builder.add_items(build_sum_of_threes_tests(10))
    builder.add_items(build_multiplication_table_tests())
    builder.add_items(build_triangle_area_tests(10))
    builder.add_items(build_sum_squares_tests(10))
    builder.add_items(build_power_tests(10))
    builder.run()


def build_sum_of_threes_tests(n):
    section = t.Section('sum_of_threes')
    tests = sum_of_threes_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_multiplication_table_tests():
    section = t.Section('multiplication_table')
    tests = multiplication_table_tests()
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}', points=10) for i, test in enumerate(tests)])
    return section


def build_triangle_area_tests(n):
    section = t.Section('triangle_area')
    tests = triangle_area_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_sum_squares_tests(n):
    section = t.Section('sum_squares')
    tests = sum_squares_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_power_tests(n):
    section = t.Section('power')
    tests = power_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


if __name__ == '__main__':
    main()
