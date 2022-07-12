import os
from pathlib import Path

from tests import test_framework as t
from tests.hw3.test_data import *

test_file = Path(os.path.dirname(hw3.__file__)) / 'hw3.py'


def main():
    builder = t.TestBuilder("hw 3", test_file, linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'if (?!__name__).*:': 'if statements not allowed for this assignment. please remove it to continue',
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue',
        '\[*\]': 'lists are not allowed for this assignment. please remove it to continue',
        'list': 'lists are not allowed for this assignment. please remove it to continue'
    })

    builder.add_items(build_average_tests(10))
    builder.add_items(build_tip_jar_tests(10))
    builder.add_items(build_newton_tests(10))
    builder.add_items(build_sequence_tests(10))
    builder.add_items(build_pi_tests(10))
    builder.run()


def build_average_tests(n):
    section = t.Section('average')
    tests = average_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_tip_jar_tests(n):
    section = t.Section('tip jar')
    tests = tip_jar_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_newton_tests(n):
    section = t.Section('newton')
    tests = newton_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_sequence_tests(n):
    section = t.Section('sequence')
    tests = sequence_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def build_pi_tests(n):
    section = t.Section('pi')
    tests = pi_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


if __name__ == '__main__':
    main()
