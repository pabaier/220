from helpers import build_test
from tests.hw7.test_data import *
from tests.test_framework import *

TEST_DIR = Path(os.path.dirname(__file__))
HW_DIR = Path(os.path.dirname(hw7.__file__)) / 'tests'
if not os.path.isdir(HW_DIR):
    os.mkdir(Path(os.path.dirname(hw7.__file__)) / 'tests')


def main():
    builder = TestBuilder("hw 7", 'hw7.py', linter_points=20, default_test_points=2)
    builder.add_to_blacklist({
        'if (?!__name__).*:': 'if statements not allowed for this assignment. please remove it to continue',
        'while.*:': 'while loops not allowed for this assignment. please remove it to continue',
        'round.*\(': 'no rounding with the round() function in this assignment'
    })
    builder.add_items(build_number_words_tests(10))
    builder.add_items(build_hourly_wages_tests(10))
    builder.add_items(build_check_sum_tests(10))
    builder.add_items(build_send_message_tests(10))
    builder.add_items(build_send_safe_message_tests(10))
    builder.add_items(build_send_uncrackable_message_tests(10))
    builder.run()


def build_number_words_tests(n):
    return build_test('number_words', number_words_tests, n)


def build_hourly_wages_tests(n):
    return build_test('hourly_wages', hourly_wages_tests, n)


def build_check_sum_tests(n):
    return build_test('check_sum', check_sum_tests, n)


def build_send_message_tests(n):
    return build_test('send_message', send_message_tests, n)


def build_send_safe_message_tests(n):
    return build_test('send_safe_message', send_safe_message_tests, n)


def build_send_uncrackable_message_tests(n):
    return build_test('send_uncrackable_message', send_uncrackable_message_tests, n)


def clean_up_files(file_names):
    for file_name in file_names:
        os.remove(file_name)
