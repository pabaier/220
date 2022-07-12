import os
from pathlib import Path

from helpers import build_test
from tests import test_framework as t
from tests.hw5.test_data import *

test_file = Path(os.path.dirname(hw5.__file__)) / 'hw5.py'


def main():
    builder = t.TestBuilder("hw 5", test_file, linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'if (?!__name__).*:': 'if statements not allowed for this assignment. please remove it to continue',
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue'
    })

    builder.add_items(build_name_reverse_tests(10))
    builder.add_items(build_company_name_tests(10))
    builder.add_items(build_initials_tests(10))
    builder.add_items(build_names_tests(10))
    builder.add_items(build_thirds_tests(10))
    builder.add_items(build_word_average_tests(9))
    builder.add_items(build_pig_latin_tests(10))
    builder.run()


def build_name_reverse_tests(n):
    return build_test('name_reverse', name_reverse_tests, n)


def build_company_name_tests(n):
    return build_test('company_name', company_name_tests, n)


def build_initials_tests(n):
    return build_test('initials', initials_tests, n)


def build_names_tests(n):
    return build_test('names', names_tests, n)


def build_thirds_tests(n):
    return build_test('thirds', thirds_tests, n)


def build_word_average_tests(n):
    return build_test('word_average', word_average_tests, n)


def build_pig_latin_tests(n):
    return build_test('pig_latin', pig_latin_tests, n)


if __name__ == '__main__':
    main()
