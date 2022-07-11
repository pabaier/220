import math
import random

import helpers

try:
    from assignments.hw10.sphere import Sphere
except:
    Sphere = None

from assignments.hw10 import hw10
from tests.test import Test


def fibonacci_tests(n):
    test_func = hw10.fibonacci
    tests = []

    i = []
    for _ in range(n):
        i.append(random.randint(1, 600))
    for index in range(1, n + 1):
        func_input = i[index - 1]
        expected = fib_helper(func_input)
        tests.append(
            Test(test_func, expected, (func_input,)).run()
        )
    return tests


def fib_helper(n):
    total = 1
    prev = 1
    for i in range(2, n):
        x = total
        total += prev
        prev = x
    return total


def double_investment_tests(n):
    test_func = hw10.double_investment
    tests = []

    principal_inputs = []
    rate_inputs = []
    expected_values = []
    for i in range(n):
        principal = random.randint(1, 100000)
        a = principal * 2
        rate = round(random.uniform(0.01, 0.4), 2)
        time = math.log(a / principal) / math.log(1 + rate)
        principal_inputs.append(principal)
        rate_inputs.append(rate)
        expected_values.append(math.ceil(time))

    for i in range(n):
        tests.append(
            Test(test_func, expected_values[i], (principal_inputs[i], rate_inputs[i])).run()
        )
    return tests


def syracuse_tests(n):
    test_func = hw10.syracuse
    tests = []

    test_values = [random.randint(1, 100) for _ in range(n)]
    for i in range(n):
        func_input = test_values[i]
        excpected = syracuse_helper_collatz_gen(func_input)
        tests.append(
            Test(test_func, excpected, (func_input,)).run()
        )
    return tests


def syracuse_helper_collatz_gen(n):
    l = [n]
    while n != 1:
        n = n / 2 if n % 2 == 0 else 3 * n + 1
        l.append(int(n))
    return l


def goldbach_tests(n):
    test_func = hw10.goldbach
    tests = []

    none_test_count = 1
    odds = [x for x in range(100000) if x % 2 != 0]
    evens = [x for x in range(10000) if x % 2 == 0]
    odd_test_values = random.choices(odds, k=none_test_count)
    even_test_values = random.choices(evens, k=n - none_test_count)

    for value in odd_test_values:
        tests.append(
            Test(test_func, None, (value,)).run()
        )
    for value in even_test_values:
        t = Test(test_func, None, (value,)).run()
        results = t.get_actual()
        is_list = True
        list_length = 0
        try:
            list_length = len(results)
        except:
            is_list = False

        checks = (is_list and list_length == 2) and \
                 (results[0] + results[1] == value) and \
                 ((i_p(results[0]) and i_p(results[1])))
        test = Test(lambda: True, checks).run()
        test.set_actual(results)
        test.set_expected(f'input: {value}')
        tests.append(
            test
        )
    return tests


def i_p(n):
    sqrt = math.floor(math.sqrt(n))
    for i in range(2, sqrt + 1):
        if n % i == 0:
            return False
    return True


def sphere_constructor_tests(n):
    return [Test(lambda r: Sphere(r), 'Construct Sphere with one parameter', (7,), comparator=lambda a, e: True).run()]


def sphere_instance_variables_tests(n):
    tests = [
        Test(lambda x: Sphere(x), 'radius instance variable 7', (7,),
             comparator=lambda a, e: a.radius == 7).run(),
        Test(lambda x: Sphere(x), 'radius instance variable type int', (7,),
             comparator=lambda a, e: type(a.radius) == int).run(),
        Test(lambda x: Sphere(x), 'radius instance variable 7.3', (7.3,),
             comparator=lambda a, e: a.radius == 7.3).run(),
        Test(lambda x: Sphere(x), 'radius instance variable type float', (7.3,),
             comparator=lambda a, e: type(a.radius) == float).run()
    ]
    return tests


def sphere_methods_tests(n):
    error = 0.0000000000001
    sphere_surface_area = random.uniform(1, 100)
    sa_radius = math.sqrt(sphere_surface_area / 4 / math.pi)

    volume = random.uniform(1, 100)
    v_radius = (volume * 3 / 4 / math.pi) ** (1 / 3)

    return [
        Test(lambda x: Sphere(x).get_radius(), 7.3, (7.3,)).run(),
        Test(lambda x: Sphere(x).surface_area(), sphere_surface_area, (sa_radius,),
             comparator=helpers.delta_comp_func(error)).run(),
        Test(lambda x: Sphere(x).volume(), volume, (v_radius,),
             comparator=helpers.delta_comp_func(error)).run()
    ]
