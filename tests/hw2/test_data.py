from random import randint

from assignments.hw2 import hw2
from tests.helpers import get_all_numbers_in_string, number_string_comp_func
from tests.test import Test


def sum_of_threes_tests(n):
    tests = [Test(hw2.sum_of_threes, '45', inp=('15',), ioTest=True, comparator=number_string_comp_func()).run()]

    for i in range(n - 1):
        s = 0
        c = 1
        upper_bound = randint(1, 50)
        while c <= upper_bound:
            if c % 3 == 0:
                s += c
            c += 1
        tests.append(Test(hw2.sum_of_threes, str(s), inp=(str(upper_bound),), ioTest=True,
                          comparator=number_string_comp_func()).run())

    return tests


def multiplication_table_tests():
    tests = []
    expected = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20'],
                ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30'],
                ['4', '8', '12', '16', '20', '24', '28', '32', '36', '40'],
                ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50'],
                ['6', '12', '18', '24', '30', '36', '42', '48', '54', '60'],
                ['7', '14', '21', '28', '35', '42', '49', '56', '63', '70'],
                ['8', '16', '24', '32', '40', '48', '56', '64', '72', '80'],
                ['9', '18', '27', '36', '45', '54', '63', '72', '81', '90'],
                ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100']]

    def comp_func():
        def a(actual, exp):
            out_list = []
            for res in actual:
                out_list.append(get_all_numbers_in_string(res))
            if not len(out_list) == len(exp): return False
            for i, line in enumerate(exp):
                if not line == out_list[i]:
                    return False
            return True

        return a

    tests.append(Test(hw2.multiplication_table, expected, ioTest=True,
                      comparator=comp_func()).run())

    return tests


def triangle_area_tests(n):
    tests = [
        Test(hw2.triangle_area, '6.0', inp=('3', '4', '5'), ioTest=True, comparator=number_string_comp_func()).run()]

    for i in range(n - 1):
        side_a = randint(2, 20)
        side_b = randint(2, 20)
        big = max([side_a, side_b])
        side_c = randint(abs(side_b - side_a) + 1, big)
        d = (side_a + side_b + side_c) / 2
        acc = d
        for i in [side_a, side_b, side_c]:
            acc *= d - i
        tests.append(
            Test(hw2.triangle_area, str(acc ** (1 / 2)), inp=(str(side_a), str(side_b), str(side_c)), ioTest=True,
                 comparator=number_string_comp_func()).run())

    return tests


def sum_squares_tests(n):
    tests = [
        Test(hw2.sum_squares, '50', inp=('3', '5'), ioTest=True, comparator=number_string_comp_func()).run()]

    for i in range(n - 1):
        lower = randint(0, 10)
        upper = randint(lower + 1, 20)
        r = range(lower, upper + 1)
        acc = sum([x * x for x in r])
        tests.append(
            Test(hw2.sum_squares, str(acc), inp=(str(lower), str(upper)), ioTest=True,
                 comparator=number_string_comp_func()).run())

    return tests


def power_tests(n):
    def comp_func(act, exp):
        return exp in act[0]

    tests = [
        Test(hw2.power, '8', inp=('2', '3'), ioTest=True, comparator=comp_func).run()]

    for i in range(n - 1):
        base = randint(1, 10)
        exponent = randint(1, 10)
        answer = base ** exponent
        tests.append(
            Test(hw2.power, str(answer), inp=(str(base), str(exponent)), ioTest=True,
                 comparator=comp_func).run())

    return tests
