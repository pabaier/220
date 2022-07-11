import os
import shutil
from pathlib import Path
from random import randint, uniform, choice

from assignments.hw7 import hw7
from tests.helpers import make_random_sentence, get_random_string, get_random_letter
from tests.hw6.test_data import encode_better_helper, encode_helper
from tests.test import Test

TEST_DIR = Path(os.path.dirname(__file__))
HW_DIR = Path(os.path.dirname(hw7.__file__)) / 'tests'
if not os.path.isdir(HW_DIR):
    os.mkdir(Path(os.path.dirname(hw7.__file__)) / 'tests')


def number_words_tests(n):
    test_name = 'number_words'
    tests = []

    shutil.copy(TEST_DIR / 'number_words_1_expected.txt', HW_DIR / 'number_words_1_expected.txt')
    shutil.copy(TEST_DIR / 'number_words_2_expected.txt', HW_DIR / 'number_words_2_expected.txt')
    shutil.copy(TEST_DIR / 'number_words_1_input.txt', HW_DIR / 'number_words_1_input.txt')
    shutil.copy(TEST_DIR / 'number_words_2_input.txt', HW_DIR / 'number_words_2_input.txt')
    expected1 = open(HW_DIR / 'number_words_1_expected.txt', 'r').read()
    expected2 = open(HW_DIR / 'number_words_2_expected.txt', 'r').read()

    file_names = [f'{test_name}_{i}_input.txt' for i in range(3, n + 1)]
    input_files_content = []
    expected_output_files_content = []
    for i in range(len(file_names)):
        i, e = number_words_generator()
        input_files_content.append(i)
        expected_output_files_content.append(e)

    create_test_files(file_names, input_files_content)

    expecteds = [expected1, expected2] + expected_output_files_content

    def comp_func(out_file_name):
        def cf(_, expected):
            actual = open(out_file_name, 'r').read()
            return actual == expected

        return cf

    for i in range(1, n + 1):
        expected = expecteds[i - 1]
        output_file_name = HW_DIR / f'{test_name}_{i}_actual.txt'
        tests.append(Test(
            hw7.number_words, expected, (HW_DIR / f'{test_name}_{i}_input.txt', output_file_name),
            comparator=comp_func(output_file_name)).run()
                     )

    return tests


def number_words_generator():
    input_file = []
    output_file = []
    lines = randint(1, 7)
    count = 1
    for i in range(lines):
        word_count = randint(1, 5)
        sentence = make_random_sentence(word_count)
        words = sentence.split()
        for word in words:
            output_file.append(f'{count} {word}')
            count += 1
        input_file.append(sentence)
    return ('\n'.join(input_file), '\n'.join(output_file) + '\n')


def hourly_wages_tests(n):
    test_name = 'hourly_wages'
    tests = []

    shutil.copy(TEST_DIR / f'{test_name}_1_expected.txt', HW_DIR / f'{test_name}_1_expected.txt')
    shutil.copy(TEST_DIR / f'{test_name}_1_input.txt', HW_DIR / f'{test_name}_1_input.txt')
    expected1 = open(HW_DIR / f'{test_name}_1_expected.txt', 'r').read()

    file_names = [f'{test_name}_{i}_input.txt' for i in range(2, n + 1)]

    input_files_content = []
    expected_output_files_content = []
    for i in range(len(file_names)):
        i, e = hourly_wages_generator()
        input_files_content.append(i)
        expected_output_files_content.append(e)

    create_test_files(file_names, input_files_content)

    expecteds = [expected1] + expected_output_files_content

    def comp_func(out_file_name):
        def cf(_, expected):
            actual = open(out_file_name, 'r').read()
            return actual == expected

        return cf

    for i in range(1, n + 1):
        expected = expecteds[i - 1]
        output_file_name = HW_DIR / f'{test_name}_{i}_actual.txt'
        tests.append(
            Test(hw7.hourly_wages, expected, (HW_DIR / f'{test_name}_{i}_input.txt', output_file_name),
                 comparator=comp_func(output_file_name)).run()
        )
    return tests


def hourly_wages_generator():
    input_file = []
    output_file = []
    number_of_names = randint(1, 7)
    for i in range(number_of_names):
        name = get_random_string() + ' ' + get_random_string()
        wage = round(uniform(15, 50), 2)
        hours = randint(10, 50)
        total = round((wage + 1.65) * hours, 2)
        input_file.append(f'{name} {wage:.2f} {hours}')
        output_file.append(f'{name} {total:.2f}')
    return ('\n'.join(input_file), '\n'.join(output_file) + '\n')


def check_sum_tests(n):
    tests = []
    inout = create_check_sum_io(n - 1)
    inout.insert(0, ('0-072-94652-0', 187))
    inputs = [x[0] for x in inout]
    for i, res in enumerate(inout):
        inp, expected = res
        tests.append(
            Test(hw7.calc_check_sum, expected, (inputs[i],)).run()
        )
    return tests


def create_check_sum_io(num):
    results = []
    for i in range(num):
        options = [False, False, False, True]
        isbn = []
        isbn_mult = []
        for multiplier in range(10, 2, -1):
            num = randint(0, 9)
            isbn.append(num)
            isbn_mult.append(num * multiplier)
        isbn_temp_sum = sum(isbn_mult)
        off_by = 11 - isbn_temp_sum % 11  # this is what we need to add to the isbn to make sure it can % 11 evenly
        if off_by >= 10:
            second = randint(1, 5)
        elif off_by == 1:
            second = 0
        else:
            second = randint(1, off_by // 2)
        isbn.append(second)
        isbn_mult.append(second * 2)
        off_by -= second * 2
        isbn.append(off_by)
        isbn_mult.append(off_by)
        i = 1
        while i < len(isbn):
            res = choice(options)
            if res:
                isbn.insert(i, '-')
                i += 1
            i += 1
        isbn = [str(x) for x in isbn]
        results.append((''.join(isbn), sum(isbn_mult)))

    return results


def send_message_tests(n):
    test_name = 'send_message'
    tests = []
    file_names = [f'{test_name}_{i}_input.txt' for i in range(1, n + 1)]

    input_files_content = []
    expected_output_files_content = []
    for i in range(len(file_names)):
        i, e = send_message_generator()
        input_files_content.append(i)
        expected_output_files_content.append(e)

    create_test_files(file_names, input_files_content)

    def comp_func(out_file_name):
        def cf(_, expected):
            actual = open(out_file_name, 'r').read()
            return actual == expected

        return cf

    for i in range(1, n + 1):
        expected = expected_output_files_content[i - 1]
        output_file_name_arg = HW_DIR / f'{test_name}_{i}_actual'
        output_file_name = HW_DIR / f'{test_name}_{i}_actual.txt'
        tests.append(
            Test(hw7.send_message, expected, (HW_DIR / f'{test_name}_{i}_input.txt', str(output_file_name_arg)),
                 comparator=comp_func(output_file_name)).run()
        )

    return tests


def send_message_generator():
    input_file = []
    output_file = []
    number_of_lines = randint(1, 100)
    for i in range(number_of_lines):
        number_of_words = randint(1, 100)
        line = []
        for j in range(number_of_words):
            line.append(get_random_string())
        input_file.append(' '.join(line))
        output_file.append(' '.join(line))
    return ('\n'.join(input_file), '\n'.join(output_file) + '\n')


def send_safe_message_tests(n):
    test_name = 'send_safe_message'
    tests = []
    file_names = [f'{test_name}_{i}_input.txt' for i in range(1, n + 1)]
    keys = [randint(0, 25) for _ in range(len(file_names))]

    input_files_content = []
    expected_output_files_content = []
    for i in range(len(file_names)):
        i, e = send_safe_message_generator(keys[i])
        input_files_content.append(i)
        expected_output_files_content.append(e)

    create_test_files(file_names, input_files_content)

    def comp_func(out_file_name):
        def cf(_, expected):
            actual = open(out_file_name, 'r').read()
            return actual == expected

        return cf

    for i in range(1, n + 1):
        expected = expected_output_files_content[i - 1]
        output_file_name_arg = HW_DIR / f'{test_name}_{i}_actual'
        output_file_name = HW_DIR / f'{test_name}_{i}_actual.txt'
        tests.append(
            Test(hw7.send_safe_message, expected,
                 (HW_DIR / f'{test_name}_{i}_input.txt', str(output_file_name_arg), keys[i - 1]),
                 comparator=comp_func(output_file_name)).run()
        )

    # check if encode function is in encryption.py

    return tests


def send_safe_message_generator(shift):
    input_file = []
    output_file = []
    for i in range(randint(1, 7)):
        sentence, _, expected = encode_helper(shift)
        input_file.append(sentence)
        output_file.append(expected)
    return ('\n'.join(input_file), '\n'.join(output_file) + '\n')


def send_uncrackable_message_tests(n):
    test_func = hw7.send_uncrackable_message
    test_name = 'send_uncrackable_message'

    file_names = [f'{test_name}_{i}_input.txt' for i in range(1, n + 1)]
    pad_file_names = [f'{test_name}_{i}_pad.txt' for i in range(1, n + 1)]

    input_files_content = []
    expected_output_files_content = []
    pad_files_content = []
    for i in range(len(file_names)):
        sentence, key, exp = send_uncrackable_message_generator()
        input_files_content.append(sentence)
        expected_output_files_content.append(exp)
        pad_files_content.append(key)

    create_test_files(file_names, input_files_content)
    create_test_files(pad_file_names, pad_files_content)

    def comp_func(out_file_name):
        def cf(actual, expected):
            actual = open(out_file_name, 'r').read()
            return actual == expected

        return cf

    tests = []
    for i in range(1, n + 1):
        exp = expected_output_files_content[i - 1]
        output_file_name_arg = HW_DIR / f'{test_name}_{i}_actual'
        output_file_name = HW_DIR / f'{test_name}_{i}_actual.txt'

        tests.append(
            Test(test_func, exp, (
                HW_DIR / f'{test_name}_{i}_input.txt', str(output_file_name_arg), HW_DIR / f'{test_name}_{i}_pad.txt'),
                 comparator=comp_func(output_file_name)).run()
        )

    # check if encode function is in encryption.py
    # tests.append(
    #     Test(f'{test_name} - encode_better in encryption.py', 'encode_better' in dir(encryption), True,
    #          show_actual_expected=False,
    #          points=2)
    # )

    return tests


def send_uncrackable_message_generator():
    input_file = []
    pad_file = ''
    number_of_lines = randint(1, 5)
    for i in range(number_of_lines):
        number_of_words = randint(1, 5)
        line = []
        for j in range(number_of_words):
            line.append(get_random_string())
        input_file.append(' '.join(line))
    input_string = '\n'.join(input_file) + '\n'
    for _ in input_string:
        pad_file += get_random_letter()
    sentence, key, exp = encode_better_helper(pad_file, input_string)
    return sentence, key, exp + '\n'


def create_test_files(file_names, contents):
    '''
    file_names - list of file names
    contents - list of file content
    '''
    for i, file_name in enumerate(file_names):
        with open(HW_DIR / file_name, 'w') as file:
            print(contents[i], file=file)
