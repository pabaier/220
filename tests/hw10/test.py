from helpers import build_test
from tests.hw10.test_data import *
from tests.test_framework import *


def main():
    test_suit = TestSuit('HW 10')

    builder = TestBuilder("hw10.py", 'hw10.py', linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'for.*in.*:': 'for loops not allowed for this assignment. please remove it to continue',
    })
    builder.add_items(build_fibonacci_tests(10))
    builder.add_items(build_double_investment_tests(10))
    builder.add_items(build_syracuse_tests(10))
    builder.add_items(build_goldbach_tests(10))

    sphere_builder = TestBuilder("sphere", "sphere.py", linter_points=20, default_test_points=10)
    sphere_builder.add_items(build_sphere_constructor_tests())
    sphere_builder.add_items(build_sphere_instance_variables_tests())
    sphere_builder.add_items(build_sphere_methods_tests())

    test_suit.add_test_builders(builder, sphere_builder)
    test_suit.run()


def build_fibonacci_tests(n):
    return build_test('fibonacci', fibonacci_tests, n)


def build_double_investment_tests(n):
    return build_test('double_investment', double_investment_tests, n)


def build_syracuse_tests(n):
    return build_test('syracuse', syracuse_tests, n)


def build_goldbach_tests(n):
    return build_test('goldbach', goldbach_tests, n)


def build_sphere_constructor_tests():
    return build_test('sphere_constructor', sphere_constructor_tests, 1)


def build_sphere_instance_variables_tests():
    return build_test('sphere_instance_variables', sphere_instance_variables_tests, 1)


def build_sphere_methods_tests():
    return build_test('sphere_methods', sphere_methods_tests, 1)
