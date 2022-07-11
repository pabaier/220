import sys
from io import StringIO

from tests.liststream import ListStream


class Test:
    def __init__(self, function, expected, params: tuple = None, inp: tuple = (), comparator=None,
                 ioTest=False):
        """
        function: the function to run
        expected: the desired output
        params: a tuple of function inputs
            single element tuples come in the form (7,)
        inp: a tuple of stdin inputs
            single element tuples come in the form (7,)
        comparator: a function used to compare output and expected
            comp(actual, expected) -> bool
        ioTest: set true to compare u_output to expected
        f_output: the result of running the function
        u_output: a list of function output from stdout
        exception: set if an exception is thrown
        passed: True if success, otherwise false
        """

        self.function = function
        self.expected = expected
        self.params = params
        self.inp = inp
        self.comparator = comparator if comparator else lambda actual, expected: actual == expected
        self.ioTest = ioTest
        self.f_output = None
        self.u_output = None
        self.exception = None
        self.passed = False

    def run(self):
        try:
            output = ListStream()
            sys.stdout = output
            input_io = StringIO('\n'.join(self.inp))
            sys.stdin = input_io

            if self.params:
                self.f_output = self.function(*self.params)
            else:
                self.f_output = self.function()

            self.u_output = output.data

            self.check()
        except Exception as e:
            self.exception = e

        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

        return self

    def check(self, actual=None, expected=None):
        """
        checks the actual against the expected
        uses object comparator function
        default actual is the function output
        default expected is the object's expected
        """
        act = actual if actual else self.u_output if self.ioTest else self.f_output
        exp = expected if expected else self.expected
        self.passed = self.comparator(act, exp)
        return self

    def get_actual(self):
        return self.u_output if self.ioTest else self.f_output

    def set_actual(self, actual):
        if self.ioTest:
            self.u_output = actual
        else:
            self.f_output = actual

    def get_expected(self):
        return self.expected

    def get_params(self):
        return self.params

    def get_input(self):
        return self.inp

    def set_expected(self, expected):
        self.expected = expected
