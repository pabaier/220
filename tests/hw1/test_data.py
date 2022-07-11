from random import randint

from assignments.hw1 import hw1
from tests.helpers import get_all_numbers_in_string
from tests.test import Test


def calc_rec_area_tests(n):
    tests = []

    def comp_func(act, exp):
        output_nums = get_all_numbers_in_string(act[0])
        return len(output_nums) == 1 and output_nums[0] == exp

    tests.append(Test(hw1.calc_rec_area, '6', inp=('2', '3'), ioTest=True, comparator=comp_func).run())
    for i in range(n - 1):
        w = randint(0, 101)
        multiplier = randint(0, 101)
        expected = w * multiplier
        tests.append(Test(hw1.calc_rec_area, str(expected), inp=(str(w), str(multiplier)), ioTest=True,
                          comparator=comp_func).run())

    return tests


def calc_volume_tests(n):
    tests = []

    def comp_func(act, exp):
        output_nums = get_all_numbers_in_string(act[0])
        return len(output_nums) == 1 and output_nums[0] == exp

    tests.append(Test(hw1.calc_volume, '24', inp=('2', '3', '4'), ioTest=True, comparator=comp_func).run())
    for i in range(n - 1):
        w = randint(0, 101)
        multiplier_1 = randint(0, 101)
        multiplier_2 = randint(0, 101)
        expected = w * multiplier_1 * multiplier_2
        tests.append(
            Test(hw1.calc_volume, str(expected), inp=(str(multiplier_1), str(w), str(multiplier_2)), ioTest=True,
                 comparator=comp_func).run())

    return tests


def shooting_percentage_tests(n):
    tests = []
    test_function = hw1.shooting_percentage

    def comp_func(act, exp):
        output_nums = get_all_numbers_in_string(act[0])
        return len(output_nums) == 1 and output_nums[0] == exp

    tests.append(Test(test_function, '40.0', inp=('10', '4'), ioTest=True, comparator=comp_func).run())
    for i in range(n - 1):
        num = randint(0, 101)
        denom = randint(0, 101)
        expected = num / denom * 100
        tests.append(
            Test(test_function, str(expected), inp=(str(denom), str(num)), ioTest=True, comparator=comp_func).run())

    return tests


def coffee_tests(n):
    tests = []
    test_function = hw1.coffee

    def comp_func(act, exp):
        output_nums = get_all_numbers_in_string(act[0])
        return len(output_nums) == 1 and abs(float(output_nums[0]) - float(exp)) < 0.000000000001

    tests.append(Test(test_function, '24.22', inp=('2',), ioTest=True, comparator=comp_func).run())
    for i in range(n - 1):
        lbs = randint(0, 101)
        expected = 10.5 * lbs + 0.86 * lbs + 1.50
        tests.append(
            Test(test_function, str(expected), inp=(str(lbs),), ioTest=True, comparator=comp_func).run())

    return tests


def kilometers_to_miles(n):
    tests = []
    test_function = hw1.kilometers_to_miles

    def comp_func(act, exp):
        output_nums = get_all_numbers_in_string(act[0])
        return len(output_nums) == 1 and abs(float(output_nums[0]) - float(exp)) < 0.027

    tests.append(Test(test_function, '1.0', inp=('1.61',), ioTest=True, comparator=comp_func).run())
    for i in range(n - 1):
        clicks = randint(1, 101)
        expected = clicks / 1.61
        tests.append(
            Test(test_function, str(expected), inp=(str(clicks),), ioTest=True, comparator=comp_func).run())

    return tests
