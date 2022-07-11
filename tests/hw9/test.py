from helpers import build_test
from tests.hw9.test_data import *
from tests.test_framework import *


def main():
    builder = TestBuilder("hw 9", 'hw9.py', linter_points=20, default_test_points=2)
    builder.add_items(build_get_words_test(10))
    builder.add_items(build_get_random_word_test(10))
    builder.add_items(build_letter_in_secret_word_test(10))
    builder.add_items(build_already_guessed_test(10))
    builder.add_items(build_make_hidden_secret_test(10))
    builder.add_items(build_won_test(10))
    builder.add_items(build_playing_test())
    builder.run()


def build_get_words_test(n):
    return build_test('get_words', get_words_test, n)


def build_get_random_word_test(n):
    return build_test('get_random_word', get_random_word_test, n)


def build_letter_in_secret_word_test(n):
    return build_test('letter_in_secret_word', letter_in_secret_word_test, n)


def build_already_guessed_test(n):
    return build_test('already_guessed', already_guessed_test, n)


def build_make_hidden_secret_test(n):
    return build_test('build_make_hidden_secret', make_hidden_secret_test, n)


def build_won_test(n):
    return build_test('won', won_test, n)


def build_playing_test():
    return build_test('playing', playing_test, 1)
