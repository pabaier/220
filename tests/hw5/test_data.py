import re
from random import randint

from assignments.hw5 import hw5
from tests.helpers import get_random_letter, get_random_string, make_random_sentence
from tests.test import Test


def name_reverse_tests(n):
    test_func = hw5.name_reverse

    def comp_func(actual: str, expected):
        return expected[0] in actual[0]

    tests = []
    for i in range(n):
        first_name = get_random_string()
        last_name = get_random_string()
        exp = f'{last_name}, {first_name}'
        tests.append(
            Test(test_func, (exp,), inp=(f"{first_name} {last_name}",), ioTest=True, comparator=comp_func).run()
        )
    return tests


def company_name_tests(n):
    test_func = hw5.company_name

    def comp_func(actual, expected):
        return expected[0] in actual[0] and 'www.' not in actual[0] and '.com' not in actual[0]

    tests = []
    for i in range(n):
        url = get_random_string()
        input_data = f"www.{url}.com"
        expected = url
        tests.append(
            Test(test_func, (expected,), inp=(input_data,), ioTest=True, comparator=comp_func).run()
        )
    return tests


def initials_tests(n):
    test_func = hw5.initials

    tests = []
    for i in range(n):
        number_of_students = randint(1, 4)
        input_data = [str(number_of_students)]
        names = []
        for _ in range(number_of_students):
            first_name = get_random_string()
            last_name = get_random_string()
            names.append((first_name, last_name, f'{first_name[0]}{last_name[0]}'))
            input_data.append(f'{first_name} {last_name}')

        def comp_func(actual, expected):
            all_good = True
            for j, name in enumerate(expected):
                exp = name[2]
                try:
                    act_index = actual[j].rfind(exp)
                    if act_index + len(exp) != len(actual[j]):
                        all_good = False
                        break
                except:
                    all_good = False
                    break
            return all_good

        tests.append(Test(test_func, names, inp=input_data, comparator=comp_func, ioTest=True).run())
    return tests


def names_tests(n):
    test_func = hw5.names
    tests = []

    def comp_func(actual, expected):
        full_output = ''.join(actual)
        res = re.search(expected, full_output)
        if res:
            return True
        return False

    for i in range(n):
        number_of_names = randint(1, 10)
        names = []
        initials = []
        initials_regex = ''
        for _ in range(number_of_names):
            first_name = get_random_string()
            last_name = get_random_string()
            names.append(f'{first_name} {last_name}')
            initials.append(f'{first_name[0]}{last_name[0]}')
            initials_regex += f'{first_name[0]}{last_name[0]}.*'

        input_data = ", ".join(names)
        tests.append(Test(test_func, initials_regex, inp=(input_data,), comparator=comp_func, ioTest=True).run())

    return tests


def thirds_tests(n):
    test_func = hw5.thirds
    tests = []

    def comp_func(actual, expected):
        all_good = True
        for j, exp in enumerate(expected):
            try:
                out = actual[j]
                res = re.search(f'.*{exp}.*', out)
                if not res: all_good = False
            except:
                all_good = False
        return all_good

    for i in range(n):
        number_of_sentences = randint(1, 4)
        input_data = [str(number_of_sentences)]
        expected_output_data = []
        for _ in range(number_of_sentences):
            sentence = make_random_sentence(randint(1, 7))
            input_data.append(sentence)
            expected_output_data.append(sentence[::3])

        tests.append(
            Test(test_func, expected_output_data, inp=input_data, comparator=comp_func, ioTest=True).run()
        )

    return tests


def word_average_tests(n):
    test_func = hw5.word_average

    def comp_func(actual, expected):
        return expected[0] in actual[0]

    tests = [
        Test(test_func, ("3.888888888888889",), inp=('the quick brown fox jumps over the lazy dog',),
             comparator=comp_func, ioTest=True).run()
    ]
    for i in range(n):
        word_count = randint(1, 7)
        sentence = make_random_sentence(word_count)
        # complicated way of getting the letter counts
        total = 0
        for l in sentence:
            if l != ' ':
                total += 1
        expected = total / word_count
        tests.append(
            Test(test_func, (str(expected),), inp=(sentence,), comparator=comp_func, ioTest=True).run()
        )
    return tests


def pig_latin_tests(n):
    test_func = hw5.pig_latin

    def comp_func(actual, expected):
        res = re.search(f'.*{expected[0]}.*', ''.join(actual))
        if res:
            return True
        return False

    tests = []
    for i in range(n):
        word_count = randint(1, 7)
        sentence_list = []
        pig_sentence_list = []
        for _ in range(word_count):
            word = get_random_string(0, 7)
            letter = get_random_letter()
            sentence_list.append(letter + word)
            pig_sentence_list.append(word + letter + 'ay')
        sentence = ' '.join(sentence_list)
        pig_sentence = ' '.join(pig_sentence_list)

        tests.append(
            Test(test_func, (pig_sentence.lower(),), inp=(sentence,), ioTest=True, comparator=comp_func).run()
        )

    return tests
