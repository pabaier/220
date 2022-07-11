import re
from random import randint, choice
from tests import test_framework as t


def build_test(name, test_func, number=None):
    section = t.Section(name)
    tests = test_func() if not number else test_func(number)
    section.add_items(*[t.TestDisplay(test, f'test {i + 1}') for i, test in enumerate(tests)])
    return section


def get_random_letter():
    return choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')


def get_random_string(min=1, max=7):
    output = ''
    length = randint(min, max)
    for i in range(length):
        output += get_random_letter()
    return output


def make_random_sentence(words=5, word_min=1, word_max=7):
    sentence = []
    for i in range(words):
        sentence.append(get_random_string(word_min, word_max))
    return ' '.join(sentence)


def get_all_numbers_in_string(line):
    """
    given a string (like IO output from a program)
    this will collect all the numbers in the string and return them as a list
    """
    # \d+ matched one or more digit
    # \. escapes the . so it is treated like a decimal
    # | logical or
    # so this gets floats | ints
    return re.findall("\d+\.\d+|\d+", line)


def score_to_letter(score: float):
    if score >= 93:
        return 'A'
    if score >= 90:
        return 'A-'
    if score >= 87:
        return 'B+'
    if score >= 83:
        return 'B'
    if score >= 80:
        return 'B-'
    if score >= 77:
        return 'C+'
    if score >= 73:
        return 'C'
    if score >= 70:
        return 'C-'
    if score >= 67:
        return 'D+'
    if score >= 63:
        return 'D'
    if score >= 60:
        return 'D-'
    return 'F'


def gen(lst):
    """
    used for looping through test input and results
    this will lazily get the value of lst and feed it to a lazily called function
    (like a lambda)
    result is used with next method
    ex: user_in = gen([1,2,3])
        element = next(user_in)
    """
    i = 0
    while True:
        yield lst[i % len(lst)]
        i += 1


def delta_comp_func(error_range):
    def a(actual, expected):
        return abs(float(actual) - float(expected)) < error_range

    return a


def delta_num_str_comp_func(error_range):
    def a(actual, expected):
        output_nums = get_all_numbers_in_string(actual[0])
        return len(output_nums) == 1 and abs(float(output_nums[0]) - float(expected)) < error_range

    return a


def number_string_comp_func():
    def a(actual, expected):
        output_nums = get_all_numbers_in_string(actual[0])
        return len(output_nums) == 1 and output_nums[0] == expected

    return a


def get_random_name():
    return get_random_string(3, 10)


def get_random_full_name():
    return get_random_name() + ' ' + get_random_name()
