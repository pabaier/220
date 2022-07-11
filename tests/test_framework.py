import re
import sys
from io import StringIO

from pylint import epylint as lint

from tests.helpers import score_to_letter, gen, get_all_numbers_in_string
from tests.liststream import ListStream
from tests.test import Test


class TestItem:
    def __init__(self, name: str, default_points: int):
        # default points are how much an individual test is worth
        #   this is so a section can have a default for all of the questions in the section
        # total points are the sum of the total possible points.
        self.default_points = default_points
        self.total_points = 0
        self.earned_points = 0
        self.name = name
        self.level = 1

    def run(self):
        pass


class TestDisplay(TestItem):
    def __init__(self, test: Test, name, points=None, fail_fast=False, show_actual_expected=True, message=None,
                 **kwargs):
        """
        Display a Test.
        :param test: the test
        :param name: the name of the test
        :param points: the amount of points the test is worth
        :param fail_fast: exit the test suit if the test fails
        :param show_actual_expected: show the actual and expected values if a test fails
        :param message: a list of messages to be displayed on failure
        """
        super().__init__(name, points)
        self.test = test
        self.fail_fast = fail_fast
        self.show_actual_expected = show_actual_expected
        self.message = message
        self.letter_grades = True if 'letter_grades' not in kwargs else kwargs['letter_grades']

    def passed(self):
        self.earned_points += self.default_points
        self.total_points += self.default_points
        tabs = '\t' * self.level
        grade = '\N{check mark}' if self.letter_grades else f'+{self.total_points}'
        print(f"{tabs}PASSED: {grade} - {self.name}")

    def failed(self):
        """
        e is an exception. this would happen when running tests on functions.
        if an exception occurs, we do not show the actual and expected values
        """
        self.total_points += self.default_points
        tabs = '\t' * self.level
        grade = '\N{ballot x}' if self.letter_grades else f'-{self.default_points}'
        print(f'{tabs}FAILED: {grade} - {self.name}')
        if self.fail_fast:
            sys.exit()
        if self.test.exception:
            print(f'{tabs}\tan exception was thrown while running this test:')
            print(f'{tabs}\t\t\t{self.test.exception}')
        if self.message:
            for line in self.message:
                print(f'{tabs}\t{line}')
        if self.show_actual_expected:
            print(f'{tabs}\tactual: {self.test.get_actual()} | expected: {self.test.get_expected()}')
        if self.test.get_input():
            print(f'{tabs}\tdata:')
            print(f'{tabs}\t\t{self.test.get_input()}')
        if self.test.get_params():
            print(f'{tabs}\tparameters:')
            print(f'{tabs}\t\t{self.test.get_params()}')

    def run(self, level=1):
        self.level = level

        if self.test.passed:
            self.passed()
        else:
            self.failed()


class Section(TestItem):
    def __init__(self, name, points=None, custom_total_points=None, group_data=None, **kwargs):
        """
        A section of a Test Suite. Can be made up of other sections and/or individual :class:`Test <tests.test_framework.TestItem>`

        :param name: the name of the section
        :param points: the default number of points to be awarded for each item in the section
        :param custom_total_points: if set, these points are awarded up front and points are subtracted for wrong answers
        :param group_data: if set, data will be displayed for the entire section if a test fails rather than individual tests
        """
        super().__init__(name, points)
        self.outline: list[TestItem] = []
        self.custom_total_points = custom_total_points
        # case where points are assigned up front and subtracted for wrong answers
        if not custom_total_points is None:
            self.total_points = custom_total_points
            self.earned_points = custom_total_points
        # used to indicate if one set of test data should be used for all the tests
        self.group_data = group_data
        self.letter_grades = True if 'letter_grades' not in kwargs else kwargs['letter_grades']

    def add_items(self, *items: TestItem):
        for item in items:
            self.outline.append(item)

    def run(self, level=1):
        tabs = '\t' * level
        start_label = f' {self.name} start '
        print()
        print('{0}{1:-^70}'.format(tabs, start_label))
        for item in self.outline:
            if item.default_points is None:
                item.default_points = self.default_points
            item.run(level + 1)
            if self.custom_total_points is None:
                self.total_points += item.total_points
                self.earned_points += item.earned_points
            # case where points are assigned up front and subtracted for wrong answers
            else:
                self.earned_points -= item.total_points
        if self.group_data and self.earned_points < self.total_points:
            print(f'{tabs}\tdata:')
            for line in self.group_data:
                print(f'{tabs}\t\t{line}')
        score = 0 if self.total_points == 0 else self.earned_points * 100 / self.total_points
        grade = score_to_letter(score) if self.letter_grades else f'{self.earned_points}/{self.total_points}'
        end_label = f' {self.name} end: {grade} '
        print('{0}{1:-^70}'.format(tabs, end_label))


class TestBuilder:
    """
    A TestBuilder

    Attributes
         blacklist:    dict of code that should not be used and the message to display if found
         rc_file:   the file to use for linting tests
         blacklist_func: the function that runs for blacklist tests. takes a tuple parameter with the blacklist and the file_name
                         this can be overridden so no blacklist tests run by setting this to lambda x : None
        lint_func:  the function that runs for linting tests. takes a tuple parameter with the file_name, linter_points, and rc_file
                    this can be overridden so no linting tests run by setting this to lambda x : None


    """

    def __init__(self, name, file_name, linter_points, default_test_points=1, **kwargs):
        """
        The builder of a test suite. Can be made up of sections and/or individual tests`

        :param name: the name of the test
        :param file_name: the name of the file being tested
        :param linter_points: the number of points assigned to linting tests
        :param default_test_points: the default number of points to be awarded for each TestItem in the test suite
        """
        self.outline: list[TestItem] = []
        self.total_points = 0
        self.earned_points = 0
        self.default_test_points = default_test_points
        self.name = name
        self.blacklist = {
            'import.*os': 'no need for the os module. please remove it to continue.',
            'from.*os': 'no need for the os module. please remove it to continue.',
            'import.*pathlib': 'no need for the pathlib module. please remove it to continue.',
            'from.*pathlib': 'no need for the pathlib module. please remove it to continue.',
            '\[.*for.*in.*\]': 'list comprehension is not allowed. please remove it to continue',
            'with.*open': 'please open files using the techniques discussed in class',
            '\..*write.*(.*)': 'please write to files using the techniques discussed in class',
            'yield': 'we do not cover yield in this class. please remove it to continue'
        }
        self.file_name = file_name
        self.rc_file = '../../.pylintrc'
        self.linter_points = linter_points
        self.blacklist_func = create_blacklist_test()
        self.lint_func = create_lint_test()
        self.lint_tests = []
        self.letter_grades = True if 'letter_grades' not in kwargs else kwargs['letter_grades']

    def add_to_blacklist(self, items: dict):
        """
        adds the items in the dictionary to the existing blacklist
        """
        self.blacklist.update(items)

    def add_items(self, *items: TestItem):
        for item in items:
            self.outline.append(item)
        return self

    def add_lint_test(self, file_name, points=None, rc_file=None):
        if points is None: points = self.linter_points
        if rc_file is None: rc_file = self.rc_file
        self.lint_tests.append(self.lint_func((file_name, points, rc_file)))

    def run(self, level=0):
        tabs = '\t' * level
        print()
        print()

        ### BLACKLIST TESTS ###
        self.blacklist_func((self.blacklist, self.file_name))
        #######

        ### LINTING TESTS ###
        lint_test = self.lint_func((self.file_name, self.linter_points, self.rc_file))
        if lint_test:
            self.outline.append(lint_test)
        for test in self.lint_tests:
            self.outline.append(test)
        #######

        test_intro = f' Starting test {self.name} '
        print('{0}{1:=^80}'.format(tabs, test_intro))
        for item in self.outline:
            if item.default_points is None:
                item.default_points = self.default_test_points
            item.run(level=level + 1)
            self.total_points += item.total_points
            self.earned_points += item.earned_points
        print()
        grade = score_to_letter(
            self.earned_points * 100 / self.total_points) if self.letter_grades else f'{self.earned_points}/{self.total_points}'
        test_outro = f' Test {self.name} complete: {grade} '
        print('{0}{1:=^80}'.format(tabs, test_outro))


class TestSuit:
    """
    A TestSuit
    """

    def __init__(self, name, **kwargs):
        """
        The test suite. Made up of test builders`
        :param name: the name of the test

        """
        self.outline: list[TestBuilder] = []
        self.total_points = 0
        self.earned_points = 0
        self.name = name
        self.letter_grades = True if 'letter_grades' not in kwargs else kwargs['letter_grades']

    def add_test_builders(self, *items: TestBuilder):
        for item in items:
            self.outline.append(item)
        return self

    def run(self):
        print()
        print()

        test_intro = f' Starting tests {self.name} '
        print('{0:=^80}'.format(test_intro))
        print()
        for item in self.outline:
            item.run(level=1)
            self.total_points += item.total_points
            self.earned_points += item.earned_points
        print()
        grade = score_to_letter(
            self.earned_points * 100 / self.total_points) if self.letter_grades else f'{self.earned_points}/{self.total_points}'
        test_outro = f' Test {self.name} complete: {grade} '
        print('{0:=^80}'.format(test_outro))


def run_safe(test):
    """
    helper function to try running a function
    test should be a lambda so it gets executed lazily in this try/catch
    returns a tuple (boolean outcome, any result)
    """
    try:
        outcome_result = (True, test())
    except Exception as e:
        outcome_result = (False, e)
    return outcome_result


def create_lint_test():
    def create_lint_section(x) -> Section:
        test_file, points, rc_file = x
        linting = Section(f'Linting {test_file}', custom_total_points=points)
        (pylint_stdout, pylint_stderr) = lint.py_run(f'{test_file} --rcfile {rc_file}', return_std=True)
        output = pylint_stdout.getvalue()
        error_list = output.split("\n")[1:-1]
        if error_list:
            test_points = len(error_list)
            error_message = error_list[:10]
            if len(error_list) > points:
                error_message.append(f'...and {len(error_list) - 10} more errors')
                test_points = points
            linting.add_items(
                TestDisplay(Test(lambda: None, True).run(), "Linting Errors", points=test_points, show_actual_expected=False,
                            message=error_message))
        else:
            linting.add_items(
                TestDisplay(Test(lambda: None, None).run(), "Linting", points=0, show_actual_expected=False))

        return linting

    return create_lint_section


def create_blacklist_test():
    def create_blacklist_code_analyzer(x):
        blacklist, test_file = x
        exiting = False
        with open(test_file, 'r') as file:
            for index, line in enumerate(file):
                for blacklist_item in blacklist:
                    res = re.search(blacklist_item, line)
                    if res:
                        culprit = res.group()
                        print(f'Line {index + 1} - {culprit} - {blacklist[blacklist_item]}')
                        exiting = True
        if exiting:
            sys.exit(1)
    return create_blacklist_code_analyzer


def get_IO(func, input: list[str] = None):
    """
    captures the output of func
    returns a tuple of:
      the output as a list, where each line is an element in the list
      the return value of the function
      any errors that may have been thrown
    optional input argument to pass to func as mock input
    input should be a list of strings, where each element is an input
    """

    error = None
    res = None
    output = ListStream()
    sys.stdout = output
    # output = StringIO()
    if input:
        input_io = StringIO('\n'.join(input))
        sys.stdin = input_io
    try:
        res = func()
        output = output.data
    except AttributeError:
        error = 'unexpected input'
    except EOFError:
        error = 'input error.'
    except Exception as e:
        error = e
    sys.stdout = sys.__stdout__  # resets stdout
    sys.stdin = sys.__stdin__
    # output = output.getvalue().splitlines()
    return (output, res, error)


def build_IO_section(name, tests, expected, dynamic_tests, test_func, test_all_output=False, error_range=None,
                     comp_func=None):
    """
    :param name: the name of the test
    :param tests: sequence of test inputs
    :expected: sequence of expected outputs
    :dynamic_tests: dict of additional tests
        {'test':[more test inputs, ...], 'expected':[more expected outputs, ...]}
    :test_func: the function being tested
    :test_all_ouptus: compares expected list to entire output list
    :error_range: the range a float can be off by while still considered passing
    """
    section = Section(name)
    for test in dynamic_tests:
        tests.append(test['test'])
        expected.append(test['expected'])
    results = []
    for test in tests:
        results.append(get_IO(test_func, test))
    actual_results = gen(results)

    def error_comp_func(actual, expected):
        return abs(float(actual) - float(expected)) < error_range

    error_function = None
    if error_range:
        error_function = error_comp_func

    for i, ex in enumerate(expected):
        output, res, error = next(actual_results)
        test_name = f'{name} {i + 1}'
        if error:
            test = Test(test_name, None, ex, exception_message=error, data=[f'inputs: {tests[i]}'])
        elif len(output) == 0:
            test = Test(test_name, True, False, exception_message='No output',
                        data=[f'inputs: {tests[i]}', f'expected: {ex}'], show_actual_expected=False)
        else:
            full_output = " ".join(output)
            output_numbers = get_all_numbers_in_string(full_output)
            try:
                if not test_all_output:
                    output_numbers = output_numbers[0]

                test = Test(test_name, output_numbers, ex, data=[f'inputs: {tests[i]}'],
                            comp_func=comp_func or error_function)
            except:
                test = Test(test_name, f'error: incorrect output', ex, data=[f'inputs: {tests[i]}'])
        section.add_items(test)
    return section


def build_IO_string_section(name, tests, expected, dynamic_tests, test_func, num_inputs=1, test_all_output=False,
                            comp_func=None):
    """
    :param name: the name of the test
    :param tests: sequence of test inputs
    :expected: sequence of expected outputs
    :dynamic_tests: dict of additional tests
        {'test':[more test inputs, ...], 'expected':[more expected outputs, ...]}
    :test_func: the function being tested
    :num_inputs: how many inputs to ignore in the output
    :test_all_ouptus: compares expected list to entire output list
    """
    section = Section(name)
    for test in dynamic_tests:
        tests.append(test['test'])
        expected.append(test['expected'])
    results = []
    for test in tests:
        results.append(get_IO(test_func, test))
    actual_results = gen(results)

    for i, ex in enumerate(expected):
        output, res, error = next(actual_results)
        test_name = f'{name} {i + 1}'
        if error:
            test = Test(test_name, None, ex, exception_message=error, data=[f'inputs: {tests[i]}'])
        elif len(output) == 0:
            test = Test(test_name, True, False, exception_message='No output',
                        data=[f'inputs: {tests[i]}', f'expected: {ex}'], show_actual_expected=False)
        else:
            final_output = ''.join(output)
            exp = ex \
                .replace('\\', '\\\\') \
                .replace('{', '\{') \
                .replace('[', '\[') \
                .replace(']', '\]') \
                .replace('(', '\(') \
                .replace(')', '\)') \
                # .replace('.', '\.')\
            # .replace('^', '\^')\
            # .replace('$', '\$')\
            # .replace('*', '\*')\
            # .replace('+', '\+')\
            # .replace('|', '\|')
            res = re.search(f'.*{exp}.*', final_output)
            try:
                test = Test(test_name, not res == None, True, show_actual_expected=False,
                            data=[f'could not find {ex} in {final_output}', f'inputs: {tests[i]}'],
                            comp_func=comp_func)
            except:
                test = Test(test_name, f'error: incorrect output', ex, data=[f'inputs: {tests[i]}'])
        section.add_items(test)
    return section
