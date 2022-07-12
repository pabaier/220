import os
from pathlib import Path

from tests import test_framework as t
from tests.hw4.test_data import *

test_file = Path(os.path.dirname(hw4.__file__)) / 'hw4.py'


def main():
    builder = t.TestBuilder("hw 4", 'hw4.py', linter_points=5, default_test_points=4)
    builder.add_to_blacklist({
        'if (?!__name__).*:': 'if statements not allowed for this assignment. please remove it to continue',
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue',
        '\[*\]': 'lists are not allowed for this assignment. please remove it to continue',
        'list': 'lists are not allowed for this assignment. please remove it to continue'
    })

    builder.add_items(build_pi_tests(10))
    builder.run()


def build_pi_tests(n):
    section = t.Section('pi2')
    tests = pi2_tests(n)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


if __name__ == '__main__':
    main()
