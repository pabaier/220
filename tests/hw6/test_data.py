import math
from random import randint

from assignments.hw6 import hw6
from tests.helpers import make_random_sentence, get_random_string
from tests.test import Test


def cash_converter_tests(n):
    test_func = hw6.cash_converter

    def comp_func(actual: str, expected):
        return expected[0] in actual[0]

    tests = [
        Test(test_func, ("7.00",), inp=("7",), comparator=comp_func, ioTest=True).run()
    ]
    for i in range(n):
        whole = randint(0, 100)
        decimal = randint(0, 9)
        expected = f'{whole}.{decimal}0'
        test_input = f'{whole}.{decimal}' if decimal > 0 else str(whole)
        tests.append(
            Test(test_func, (expected,), inp=(test_input,), comparator=comp_func, ioTest=True).run()
        )
    return tests


def encode_tests(n):
    test_func = hw6.encode

    def comp_func(actual, expected):
        return expected[0] in actual[0] and 'www.' not in actual[0] and '.com' not in actual[0]

    tests = [
        Test(test_func, ("[ol'{ptl'ohz'jvtl3'{ol'^hsy|z'zhpk",), inp=("The time has come, the Walrus said", "7"),
             ioTest=True, comparator=comp_func).run()
    ]
    for i in range(n):
        sentence, shift, expected = encode_helper()
        tests.append(
            Test(test_func, (expected,), inp=(sentence, str(shift)), ioTest=True, comparator=comp_func).run()
        )
    return tests


def encode_helper(shift=None):
    words_in_sentence = randint(1, 7)
    s = make_random_sentence(words_in_sentence)
    sentence = ''
    for letter in s:
        sentence += chr(ord(letter) - 32)
    if not shift:
        shift = randint(0, 100)
    expected = ''.join([chr(ord(l) + shift) for l in sentence])
    return sentence, shift, expected


def sphere_area_tests(n):
    test_func = hw6.sphere_area

    def comp_func(actual, expected):
        return abs(actual - expected) < 0.0000000001

    tests = []

    for i in range(n):
        radius = randint(0, 100)
        res = 4 * math.pi * radius ** 2
        tests.append(Test(test_func, res, (radius,), comparator=comp_func).run())
    return tests


def sphere_volume_tests(n):
    test_func = hw6.sphere_volume

    def comp_func(actual, expected):
        return abs(actual - expected) < 0.000000001

    tests = []

    for i in range(n):
        radius = randint(0, 100)
        res = 4 / 3 * math.pi * radius ** 3
        tests.append(Test(test_func, res, (radius,), comparator=comp_func).run())
    return tests


def sum_n_tests(n):
    test_func = hw6.sum_n

    tests = []

    for i in range(n):
        number = randint(0, 100)
        res = sum(list(range(1, number + 1)))
        tests.append(Test(test_func, res, (number,)).run())
    return tests


def sum_n_cubes_tests(n):
    test_func = hw6.sum_n_cubes

    tests = []

    for i in range(n):
        number = randint(0, 100)
        res = sum([x ** 3 for x in range(1, number + 1)])
        tests.append(Test(test_func, res, (number,)).run())
    return tests


def encode_better_tests(n):
    test_func = hw6.encode_better

    def comp_func(actual, expected):
        return expected[0] in actual[0]

    tests = [
        Test(test_func, ("JWVVPST",), inp=("dolphin", "ace"),
             ioTest=True, comparator=comp_func).run()
    ]
    for i in range(n):
        (sentence, key, exp) = encode_better_helper()
        tests.append(
            Test(test_func, (exp,), inp=(sentence, key), ioTest=True, comparator=comp_func).run()
        )
    return tests


def encode_better_helper(key=None, sentence=None):
    words_in_sentence = randint(1, 7)
    if not sentence:
        sentence = make_random_sentence(words_in_sentence)
    sentence_nums = [ord(l) - ord('A') for l in sentence]
    if not key:
        key = get_random_string()
    test_key = (key * (len(sentence) // len(key))) + (key * (len(sentence) % len(key)))
    # take out new lines
    new_line_indexes = []
    for i, letter in enumerate(sentence):
        if letter == '\n':
            new_line_indexes.append(i)
    sentence = sentence.replace('\n', '')
    key_nums = [ord(k) - ord('A') for k in test_key]
    new_numbers = [l + key_nums[i] for i, l in enumerate(sentence_nums)]
    new_letters = [x % (ord('z') - ord('A') + 1) for x in new_numbers]
    exp = ''.join([chr(x + ord('A')) for x in new_letters])
    # add new lines back
    for index in new_line_indexes:
        sentence = sentence[0:index] + '\n' + sentence[index:]

    return sentence.rstrip('\n'), key, exp
