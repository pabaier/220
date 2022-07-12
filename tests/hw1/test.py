import os
from pathlib import Path

from tests import test_framework as t
from tests.hw1.test_data import *

test_file = Path(os.path.dirname(hw1.__file__)) / 'hw1.py'


def main():
    builder = t.TestBuilder("hw 1", test_file, linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'if (?!__name__).*:': 'if statements not allowed for this assignment. please remove it to continue',
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue',
        '\[*\]': 'lists are not allowed for this assignment. please remove it to continue',
        'list': 'lists are not allowed for this assignment. please remove it to continue'
    })
    builder.add_items(build_calc_rec_area_tests(10))
    builder.add_items(build_calc_volume_tests(10))
    builder.add_items(build_shooting_percentage_tests(10))
    builder.add_items(build_coffee_tests(10))
    builder.add_items(build_kilometers_to_miles_tests(10))
    builder.run()


def build_kilometers_to_miles_tests(n):
    section = t.Section('kilometers_to_miles')
    tests = kilometers_to_miles(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_coffee_tests(n):
    section = t.Section('coffee')
    tests = coffee_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_shooting_percentage_tests(n):
    section = t.Section('shooting_percentage')
    tests = shooting_percentage_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_calc_volume_tests(n):
    section = t.Section('calc_volume')
    tests = calc_volume_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_calc_rec_area_tests(n):
    section = t.Section('calc_rec_area')
    tests = calc_rec_area_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


if __name__ == '__main__':
    main()
