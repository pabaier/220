from helpers import build_test
from tests.hw6.test_data import *
from tests.test_framework import *


def main():
    builder = TestBuilder("hw 6", 'hw6.py', linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'if (?!__name__).*:': 'if statements not allowed for this assignment. please remove it to continue',
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue'
    })
    builder.add_items(build_cash_converter_tests(9))
    builder.add_items(build_encode_tests(9))
    builder.add_items(build_sphere_area_tests(10))
    builder.add_items(build_sphere_volume_tests(10))
    builder.add_items(build_sum_n_tests(10))
    builder.add_items(build_sum_n_cubes_tests(10))
    builder.add_items(build_encode_better_tests(9))
    builder.run()


def build_cash_converter_tests(n):
    return build_test('cash_converter', cash_converter_tests, n)


def build_encode_tests(n):
    return build_test('encode', encode_tests, n)


def build_sphere_area_tests(n):
    return build_test('sphere_area', sphere_area_tests, n)


def build_sphere_volume_tests(n):
    return build_test('sphere_volume', sphere_volume_tests, n)


def build_sum_n_tests(n):
    return build_test('sum_n', sum_n_tests, n)


def build_sum_n_cubes_tests(n):
    return build_test('sum_n_cubes', sum_n_cubes_tests, n)


def build_encode_better_tests(n):
    return build_test('encode_better', encode_better_tests, n)


if __name__ == '__main__':
    main()
