import math
import random

from graphics import *

from assignments.hw8 import hw8
from tests.test import Test


def add_ten_tests(n):
    test_func = hw8.add_ten

    def comp_func(orig_list):
        def cf(actual, expected):
            return expected == orig_list

        return cf

    tests = []
    for i in range(n):
        list_len = random.randint(0, 25)
        original_list = [random.randint(-100, 100) for _ in range(list_len)]
        add_ten_list = [x + 10 for x in original_list]
        tests.append(
            Test(test_func, add_ten_list, (original_list,), comparator=comp_func(original_list)).run()
        )
    return tests


def square_each_tests(n):
    test_func = hw8.square_each

    def comp_func(orig_list):
        def cf(actual, expected):
            return expected == orig_list

        return cf

    tests = []

    for i in range(n):
        list_len = random.randint(0, 25)
        original_list = [random.randint(-100, 100) for _ in range(list_len)]
        square_list = [x ** 2 for x in original_list]
        tests.append(
            Test(test_func, square_list, (original_list,), comparator=comp_func(original_list)).run()
        )
    return tests


def sum_list_tests(n):
    test_func = hw8.sum_list

    tests = []
    inputs = []
    for i in range(n):
        list_len = random.randint(0, 25)
        inputs.append([random.randint(-100, 100) for _ in range(list_len)])

    for i in range(n):
        tests.append(
            Test(test_func, sum(inputs[i]), (inputs[i],)).run()
        )
    return tests


def to_numbers_tests(n):
    test_func = hw8.to_numbers

    def comp_func(orig_list):
        def cf(actual, expected):
            return expected == orig_list

        return cf

    tests = []
    for i in range(n):
        list_len = random.randint(0, 25)
        original_list = [random.uniform(-100, 100) for _ in range(list_len)]
        string_list = [str(x) for x in original_list]
        tests.append(
            Test(test_func, original_list, (string_list,), comparator=comp_func(string_list)).run()
        )
    return tests


def sum_of_squares_tests(n):
    test_func = hw8.sum_of_squares

    tests = []

    for i in range(n):
        lines = random.randint(1, 7)
        line_list_strings_input = []
        line_list_nums = []
        line_list_sums_expected = []
        for j in range(lines):
            numbers_count = random.randint(1, 7)
            numbers_list = [round(random.uniform(1, 9), 2) for _ in range(numbers_count)]
            line_list_nums.append(numbers_list)
            line_list_sums_expected.append(sum([x ** 2 for x in numbers_list]))
            line_string = ', '.join([str(x) for x in numbers_list])
            line_list_strings_input.append(line_string)
        tests.append(
            Test(test_func, line_list_sums_expected, (line_list_strings_input,)).run()
        )
    return tests


def starter_tests(n):
    test_func = hw8.starter

    tests = []

    input_expected = [(150, 5, True), (150, 4, False), (149, 5, False), (160, 5, False), (161, 5, False),
                      (200, 1, True), (199, 20, False), (199, 21, True), (201, 21, True), (300, 0, True)]
    expected = [x[2] for x in input_expected]
    weight = [x[0] for x in input_expected]
    wins = [x[1] for x in input_expected]
    for i in range(len(input_expected)):
        tests.append(
            Test(test_func, expected[i], (weight[i], wins[i],)).run()
        )
    return tests


def leap_year_tests(n):
    test_func = hw8.leap_year

    tests = []
    leap_years = []
    for i in range(2020):
        year = i * 4
        check_year = str(year / 100)
        if check_year.split('.')[-1] == '0':
            if str(year / 400).split('.')[-1] == '0':
                leap_years.append(year)
        else:
            leap_years.append(year)
    all_years = [x for x in range(5000)]
    start = 0
    step = len(all_years) // n
    stop = step
    all_year_groups = []
    for i in range(n):
        all_year_groups.append(all_years[start:stop])
        start += step
        stop += step
    for test_number, year_group in enumerate(all_year_groups):
        passed_all = True
        for year in year_group:
            t = Test(test_func, year in leap_years, (year,)).run()
            t.passed
            if not t.passed:
                tests.append(t)
                passed_all = False
                break
        if passed_all:
            tests.append(
                Test(lambda x: True, True, (f'years {test_number * step} - {(test_number + 1) * step - 1}',)).run()
            )
    return tests


def did_overlap_tests(n):
    test_func = hw8.did_overlap

    tests = []

    test_result = True
    c1 = []
    c2 = []
    results = []
    for i in range(1, n + 1):
        p1_x = random.randint(-100, 100)
        p1_y = random.randint(-100, 100)
        p2_x = random.randint(-100, 100)
        p2_y = random.randint(-100, 100)
        distance = math.sqrt(math.pow(p2_x - p1_x, 2) + math.pow(p2_y - p1_y, 2))
        r1 = random.randint(1, int(distance))
        margin = 0 if test_result else 0.00001
        r2 = distance - r1 - margin
        c1.append(Circle(Point(p1_x, p1_y), r1))
        c2.append(Circle(Point(p2_x, p2_y), r2))
        results.append(test_result)
        test_result = not test_result

    for j in range(1, n + 1):
        tests.append(
            Test(test_func, results[j - 1], (c1[j - 1], c2[j - 1])).run()
        )
    return tests
