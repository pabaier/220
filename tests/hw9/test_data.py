import random
from pathlib import Path

from graphics import *

from assignments.hw9 import hw9
from helpers import get_random_string, get_random_letter
from tests.test import Test

TEST_DIR = Path(os.path.dirname(__file__))


def get_words_test(n):
    test_func = hw9.get_words

    tests = []

    words = []
    file_names = []
    for i in range(n):
        file_name = f'get_words_test_{i}'
        file_names.append(TEST_DIR / file_name)
        file = open(TEST_DIR / f'{file_name}', 'w')
        word_count = random.randint(1, 5)
        word_list = []
        for j in range(word_count):
            word = get_random_string()
            print(word, file=file)
            word_list.append(word + '\n')
        file.close()
        words.append(word_list)
    for i in range(n):
        tests.append(
            Test(test_func, words[i], (file_names[i],)).run()
        )
    return tests


def get_random_word_test(n):
    test_func = hw9.get_random_word

    tests = []

    words = []
    for i in range(n):
        number_of_words = random.randint(1, 5)
        word_list = []
        for j in range(number_of_words):
            word = get_random_string()
            word_list.append(word + '\n')
        words.append(word_list)
    for i in range(n):
        word_list = words[i]
        wl = [x[:-1] for x in word_list]
        removed = []
        error = False
        for j in range(500):
            t = Test(test_func, None, (word_list,)).run()
            result = t.get_actual()
            if result not in removed:
                try:
                    wl.remove(result)
                    removed.append(result)
                except ValueError:
                    error = True
                    break
            if len(wl) == 0:
                break
        tests.append(
            Test(lambda x: False, error, (None,)).run()
        )
    return tests


def letter_in_secret_word_test(n):
    tests = []
    test_func = hw9.letter_in_secret_word

    word = get_random_string(n // 2, n // 2)
    for i in range(len(word)):
        tests.append(
            Test(test_func, True, (word[i], word)).run()
        )

    j = 0
    un_letters = []
    while j < n // 2:
        un_letter = get_random_letter()
        if un_letter not in word:
            un_letters.append(un_letter)
            j += 1
    for k in range(len(un_letters)):
        tests.append(
            Test(test_func, False, (un_letters[k], word)).run()
        )
    return tests


def already_guessed_test(n):
    test_func = hw9.already_guessed
    tests = []
    guesses = []
    unguesses = []
    i = 0
    while i < n:
        random_letter = get_random_letter().lower()
        if random_letter not in guesses:
            guesses.append(random_letter)
            i += 1
    i = 0
    while i < n:
        random_letter = get_random_letter().lower()
        if random_letter not in guesses:
            unguesses.append(random_letter)
            i += 1
    letter_gen = random.sample(guesses, n // 2)
    for i in range(n // 2):
        tests.append(
            Test(test_func, True, (letter_gen[i], guesses)).run()
        )

    unletter_gen = random.sample(unguesses, n // 2)
    for i in range(n // 2):
        tests.append(
            Test(test_func, False, (unletter_gen[i], guesses)).run()
        )

    return tests


def make_hidden_secret_test(n):
    tests = []
    test_func = hw9.make_hidden_secret

    odds = [True, True, True, False]
    secret_words = []
    hidden_secrets = []
    guesses = []
    for i in range(n):
        secret_word = get_random_string().lower()
        secret_words.append(secret_word)
        hidden_secret = ''
        guessed_letters = []
        already_hidden_letters = []
        for letter in secret_word:
            if letter in guessed_letters:
                hidden_secret += letter + ' '
            elif random.choice(odds) and letter not in already_hidden_letters:
                hidden_secret += letter + ' '
                if letter not in guessed_letters:
                    guessed_letters.append(letter)
            else:
                hidden_secret += '_ '
                already_hidden_letters.append(letter)
        hidden_secret = hidden_secret[:-1]
        hidden_secrets.append(hidden_secret)
        extra_guesses = random.randint(0, 5)
        j = 0
        while j < extra_guesses:
            letter = get_random_letter().lower()
            if letter not in secret_word and letter not in guessed_letters:
                guessed_letters.append(letter)
                j += 1
        guesses.append(guessed_letters)

    for i in range(n):
        tests.append(
            Test(test_func, hidden_secrets[i], (secret_words[i], guesses[i])).run()
        )
    return tests


def won_test(n):
    tests = []
    test_func = hw9.won

    odds = [True, True, True, True, False]
    hidden_secrets = []
    results = []
    secret_words = []
    for i in range(n):
        secret_word = get_random_string().lower()
        secret_words.append(secret_word)
        hidden_secret = ''
        won = True
        for letter in secret_word:
            if random.choice(odds):
                hidden_secret += letter + ' '
            else:
                hidden_secret += '_ '
                won = False
        hidden_secret = hidden_secret[:-1]
        hidden_secrets.append(hidden_secret)
        results.append(won)

    for i in range(n):
        tests.append(
            Test(test_func, results[i], (hidden_secrets[i],)).run()
        )

    return tests


def playing_test(n):
    playing_tests = []
    test_func = hw9.play_command_line
    # secret word, guesses, outputs, is winner
    tests = [
        ('hello', ['h', 'e', 'l', 'o'], ['_ _ _ _ _', 'h _ _ _ _', 'h e _ _ _', 'h e l l _', 'hello'],
         True),
        ('walrus', ['w', 'a', 'e', 'o', 't', 'l', 's', 'u', 'r'],
         ['_ _ _ _ _ _', 'w _ _ _ _ _', 'w a _ _ _ _', 'w a _ _ _ _', 'w a _ _ _ _', 'w a _ _ _ _', 'w a l _ _ _',
          'w a l _ _ s', 'w a l _ u s', 'walrus'],
         True),
        ('abide', ['a', 'e', 'i', 'o', 'u', 'y', 's', 'u', 'v', 'r'],
         ['_ _ _ _ _', 'a _ _ _ _', 'a _ _ _ e', 'a _ i _ e', 'a _ i _ e', 'a _ i _ e', 'a _ i _ e', 'a _ i _ e',
          'a _ i _ e', 'a _ i _ e'],
         False),
        ('register', ['r', 'e', 'e', 'n', 'u', 'y', 's', 'u', 'v', 'r', 'j', 'k'],
         ['_ _ _ _ _ _ _ _', 'r _ _ _ _ _ _ r', 'r e _ _ _ _ e r', 'r e _ _ _ _ e r', 'r e _ _ _ _ e r',
          'r e _ _ _ _ e r', 'r e _ _ _ _ e r', 'r e _ _ s _ e r', 'r e _ _ s _ e r', 'r e _ _ s _ e r',
          'r e _ _ s _ e r', 'r e _ _ s _ e r'],
         False),
        ('lebowski', ['r', 's', 't', 'l', 'n', 'e', 'b', 'j', 'k', 'v', 'o', 'w', 'i'],
         ['_ _ _ _ _ _ _ _', '_ _ _ _ _ _ _ _', '_ _ _ _ _ s _ _', '_ _ _ _ _ s _ _', 'l _ _ _ _ s _ _',
          'l _ _ _ _ s _ _', 'l e _ _ _ s _ _', 'l e b _ _ s _ _', 'l e b _ _ s _ _', 'l e b _ _ s k _',
          'l e b _ _ s k _', 'l e b o _ s k _', 'l e b o w s k _', 'lebowski'],
         True),
    ]
    for i, test in enumerate(tests):
        word = test[0]
        input = test[1]
        expected_progress = test[2]
        did_win = test[3]
        game_play_test = Test(test_func, None, (word,), inp=input, ioTest=True).run()
        output = game_play_test.get_actual()
        hidden_progress = [x for x in output if x.find('_') >= 0 or x.replace(' ', '') == word]
        if did_win and hidden_progress:
            last: str = hidden_progress[-1]
            hidden_progress = hidden_progress[:-1]
            hidden_progress.append(last.replace(' ', ''))

        playing_tests.append(
            Test(lambda: hidden_progress, expected_progress).run()
        )
        playing_tests.append(
            Test(lambda: ''.join(output).find('winner') >= 0, did_win).run()
        )
    return playing_tests
