import math
from random import randint

from assignments.hw4 import hw4
from tests.helpers import delta_num_str_comp_func
from tests.test import Test


def pi2_tests(n):
    test_func = hw4.pi2

    def comp_func(actual: str, expected):
        one = delta_num_str_comp_func(0.0000000000001)([actual[0]], expected[0])
        two = delta_num_str_comp_func(0.0000000000001)([actual[1]], expected[1])

        return one and two

    tests = [Test(test_func, ('4.0', "0.8584073464102069"), inp=("1",), ioTest=True, comparator=comp_func).run()]

    for i in range(n - 1):
        positive = 1
        negative = -3
        sum = 0
        terms = randint(1, 1000)
        for i in range(terms):
            if i % 2 == 0:
                sum += 4 / positive
                positive += 4
            else:
                sum += 4 / negative
                negative -= 4

        tests.append(
            Test(test_func, (str(sum), str(abs(sum - math.pi))), inp=(str(terms),), ioTest=True,
                 comparator=comp_func).run()
        )
    return tests
