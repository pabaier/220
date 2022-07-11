import functools
import statistics
from random import randint, uniform

from assignments.hw3 import hw3
from tests.helpers import get_all_numbers_in_string, number_string_comp_func, delta_num_str_comp_func
from tests.test import Test


def average_tests(n):
    test_func = hw3.average
    comp_func = delta_num_str_comp_func(0.0000000000001)
    tests = [Test(test_func, '10.0', inp=('1', '10'), ioTest=True, comparator=comp_func).run()]

    for i in range(n - 1):
        num = randint(1, 20)
        ges = [randint(1, 100) for _ in range(num)]
        tests.append(
            Test(test_func, str(float(statistics.mean(ges))), inp=tuple([str(x) for x in [num] + ges]), ioTest=True,
                 comparator=comp_func).run())

    return tests


def tip_jar_tests(n):
    tests = [
        Test(hw3.tip_jar, '16.75', inp=("1", "2.25", "3.50", "4.75", "5.25"), ioTest=True,
             comparator=number_string_comp_func()).run()]

    for i in range(n - 1):
        tips = [round(uniform(0.01, 100), 2) for _ in range(5)]
        tests.append(
            Test(hw3.tip_jar, str(sum(tips)), inp=tuple([str(x) for x in tips]), ioTest=True,
                 comparator=number_string_comp_func()).run())

    return tests


def newton_tests(n):
    test_fun = hw3.newton

    tests = [
        Test(test_fun, '2.05', inp=("4", "2"), ioTest=True, comparator=number_string_comp_func()).run()]

    for i in range(n - 1):
        x = randint(1, 100)
        l = randint(0, 5)
        a = functools.reduce(lambda acc, n: (acc + x / acc) / 2, range(l), x)

        tests.append(
            Test(test_fun, str(a), inp=(str(x), str(l)), ioTest=True,
                 comparator=number_string_comp_func()).run())

    return tests


def sequence_tests(n):
    test_fun = hw3.sequence

    def comp_func(act, exp):
        output_nums = get_all_numbers_in_string(act[0])
        return output_nums == exp

    tests = [
        Test(test_fun, ["1", "1", "3", "3", "5"], inp=('5',), ioTest=True, comparator=comp_func).run()]

    for i in range(n - 1):
        terms = randint(0, 20)
        all = list(range(1, terms + 1)) * 2
        all.sort()
        vals = [x for x in all if x % 2 != 0][:terms]

        tests.append(
            Test(test_fun, [str(x) for x in vals], inp=(str(terms),), ioTest=True,
                 comparator=comp_func).run())

    return tests


def pi_tests(n):
    test_fun = hw3.pi
    comp_fun = delta_num_str_comp_func(0.0000000000001)
    tests = [Test(test_fun, '3.5555555555555554', inp=('3',), ioTest=True, comparator=comp_fun).run()]

    for i in range(n - 1):
        terms = randint(0, 1000)
        n, nums = 2, [2]
        d, dens = 1, [1]
        for i in range(terms - 1):
            if i % 2 == 1:
                n += 2
            else:
                d += 2
            nums.append(n)
            dens.append(d)
        acc = 1
        numm, denn = 1, 1
        for i, num in enumerate(nums):
            acc *= num / dens[i]
            numm *= num
            denn *= dens[i]

        tests.append(
            Test(test_fun, str(acc * 2), inp=(str(terms),), ioTest=True,
                 comparator=comp_fun).run())

    return tests
