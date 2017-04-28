#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for Gurgen programm.

Tested under:
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=14.04
DISTRIB_CODENAME=trusty
DISTRIB_DESCRIPTION="Ubuntu 14.04.3 LTS"

Python version:
Python 2.7.6
Python 2.7.10
"""

import sys
import os
import unittest


class ResultError(Exception):
    """Base custom exception class."""

    pass


class HeaderError(ResultError):
    """Header exception."""

    pass


class ResultOrderError(ResultError):
    """Wrong output order exception."""

    pass


class DiceNumberError(ResultError):
    """Exception for wrong dice number value."""

    pass


class TurnsNumberError(ResultError):
    """Exception for turns number value."""

    pass


class DiceValueError(ResultError):
    """Exception for dice value."""

    pass


class WrongResultError(ResultError):
    """Exception for wrong result."""

    pass


class WrongDataError(ResultError):
    """Exception for wrong data type in result."""

    pass


def get_points(dices):
    """Calculate turn points."""
    res = 0
    for x in dices:
        if x in (2, 3, 4, 6):
            continue
        if x == 1:
            res += 10
            continue
        if x == 5:
            res += 5
    return res


def get_points_with_combo(dices, combo={1, 2, 3, 4, 5}):
    """Calculate turn points with special combinaiton."""
    if set(dices) == combo:
        return 150
    return get_points(dices)


def parse_results(f, turns_n, min_dice_n, max_dice_n):
    """Compare turn points with turn result."""
    line = next(f)
    turns_line = "Number of turns: %s\n" % turns_n
    if line != turns_line:
        raise HeaderError("Expected %s but got %s" % (turns_line, line))
    line = next(f)
    min_dice_line = "Minimum number of dices: %s\n" % min_dice_n
    if line != min_dice_line:
        raise HeaderError("Expected %s but got %s" % (min_dice_line, line))
    line = next(f)
    max_dice_line = "Maximum number of dices: %s\n" % max_dice_n
    if line != max_dice_line:
        raise HeaderError("Expected %s but got %s" % (max_dice_line, line))
    valid_values = {1, 2, 3, 4, 5, 6}
    turns = 0
    for line in f:
        if not line.startswith("Dices: "):
            raise ResultOrderError("Expected line with dices but got: %s"
                                   % line)
        dices = line.split(": ")[-1]
        try:
            dices = tuple(int(x) for x in dices.split())
        except ValueError as e:
            raise WrongDataError("%s in %s" % (e.message, line))

        res_line = next(f)
        if not res_line.startswith("Result: "):
            raise ResultOrderError("Expected turn result, but got: %s"
                                   % res_line)

        try:
            res = int(res_line.split(": ")[-1])
        except ValueError as e:
            raise WrongDataError("%s in %s" % (e.message, res_line))
        turns += 1
        if len(dices) < min_dice_n or len(dices) > max_dice_n:
            raise DiceNumberError("Wrong dices number in %s" % line)
        if not set(dices).issubset(valid_values):
            raise DiceValueError("Unexpected values in %s" % line)
        if len(dices) == 5:
            calc_res = get_points_with_combo(dices)
        else:
            calc_res = get_points(dices)
        if calc_res != res:
            raise WrongResultError("Wrong result in %s: expected %s but got %s"
                                   % (line, calc_res, res))

    if turns != turns_n:
        raise TurnsNumberError("Expected %s turns but got %s"
                               % (turns_n, turns))


class TestGurgenArgs(unittest.TestCase):
    """Tests for Gurgen arguments."""

    programm = ""

    def testNoArgs(self):
        """Launch with no args."""
        self.assertNotEqual(os.system("%s > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "no arguments have accepted")

    def testOneArg(self):
        """Launch with 1 arg."""
        self.assertNotEqual(os.system("%s 1 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "just one has argument accepted")

    def testTwoArgs(self):
        """Launch with 2 args."""
        self.assertNotEqual(os.system("%s 1 1 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "just two have arguments accepted")

    def testMoreThanThreeArgs(self):
        """Launch with more three args."""
        self.assertNotEqual(os.system("%s 1 1 1 1 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "more than three arguments have accepted")

    def testZeroTurns(self):
        """Launch with 0 turns."""
        self.assertNotEqual(os.system("%s 0 1 1 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "zero turns have accepted")

    def testMaxTurns(self):
        """Launch with 999999 turns."""
        self.assertEqual(os.system("%s 999999 1 1 > /dev/null 2>&1"
                                   % self.programm),
                         0,
                         "max turns have not accepted")

    def testMoreThanMaxTurns(self):
        """Launch with more than max turns."""
        self.assertNotEqual(os.system("%s 1000000 1 1 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "more than max turns has accepted")

    def testMoreThanMaxDices(self):
        """Launch with more than max dices."""
        self.assertNotEqual(os.system("%s 10 1 6 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "more than max dices has accepted")

    def testLessThanMinDices(self):
        """Launch with less than min dices."""
        self.assertNotEqual(os.system("%s 10 0 5 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "more than max dices has accepted")

    def testMinDicesMoreThanMaxDices(self):
        """Launch with min dices more than max dices."""
        self.assertNotEqual(os.system("%s 10 2 1 > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "min dices more than max dices have accepted")

    def testWrongArgsType(self):
        """Launch with wrong args type."""
        self.assertNotEqual(os.system("%s a b c > /dev/null 2>&1"
                                      % self.programm),
                            0,
                            "wrong args type has accepted")

    def testArgsAsStr(self):
        """Launch with args as strings."""
        self.assertEqual(os.system("%s '1' '1' '1' > /dev/null 2>&1"
                                   % self.programm),
                         0,
                         "args as strings must be accepted")


class TestGurgen(unittest.TestCase):
    """Test for Gurgen result."""

    programm = ""

    def setUp(self):
        """Test setup."""
        os.system("cp /dev/null %s" % self._testMethodName)

    def testIfResultIsFull(self):
        """Test that output is exists/full."""
        turns = 10
        min_dices_n = 1
        max_dices_n = 2
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.fail(e.message)
            except ResultError:
                pass

    def testResultHeader(self):
        """Check header in result file."""
        turns = 100
        min_dices_n = 1
        max_dices_n = 2
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.skipTest("Skipped. Output is not full: %s" % e.message)
            except HeaderError as e:
                self.fail(e.message)
            except ResultError:
                pass

    def testResultOrder(self):
        """Check ordering in result file."""
        turns = 100
        min_dices_n = 1
        max_dices_n = 2
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.skipTest("Skipped. Output is not full: %s" % e.message)
            except HeaderError as e:
                self.skipTest(e.message)
            except ResultOrderError as e:
                self.fail(e.message)
            except ResultError:
                pass

    def testResultData(self):
        """Check data type in result file."""
        turns = 20000
        min_dices_n = 1
        max_dices_n = 2
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.skipTest("Skipped. Output is not full: %s" % e.message)
            except HeaderError as e:
                self.skipTest(e.message)
            except ResultOrderError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except WrongDataError as e:
                self.fail(e.message)
            except ResultError:
                pass

    def testDiceNumbers(self):
        """Check dice numbers in turns in result file."""
        turns = 200000
        min_dices_n = 1
        max_dices_n = 5
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.skipTest("Skipped. Output is not full: %s" % e.message)
            except HeaderError as e:
                self.skipTest(e.message)
            except ResultOrderError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except WrongDataError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except DiceNumberError as e:
                self.fail(e.message)
            except ResultError:
                pass

    def testDiceValues(self):
        """Check dice values in turns in result file."""
        turns = 200000
        min_dices_n = 1
        max_dices_n = 5
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.skipTest("Skipped. Output is not full: %s" % e.message)
            except HeaderError as e:
                self.skipTest(e.message)
            except ResultOrderError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except WrongDataError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except DiceNumberError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except DiceValueError as e:
                self.fail(e.message)
            except ResultError:
                pass

    def testTurnResult(self):
        """Check turn points in result file."""
        turns = 200000
        min_dices_n = 1
        max_dices_n = 5
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.skipTest("Skipped. Output is not full: %s" % e.message)
            except HeaderError as e:
                self.skipTest(e.message)
            except ResultOrderError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except WrongDataError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except DiceNumberError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except DiceValueError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except WrongResultError as e:
                self.fail(e.message)
            except ResultError:
                pass

    def testTurnsNumberResult(self):
        """Check turns number in result file."""
        turns = 200000
        min_dices_n = 1
        max_dices_n = 5
        cmd = "%s %s %s %s > %s" % (self.programm,
                                    turns, min_dices_n,
                                    max_dices_n,
                                    self._testMethodName)
        if os.system(cmd):
            self.skipTest("%s command has been executed with error" % cmd)
        with open(self._testMethodName, "r") as f:
            try:
                parse_results(f, turns, min_dices_n, max_dices_n)
            except StopIteration as e:
                self.skipTest("Skipped. Output is not full: %s" % e.message)
            except HeaderError as e:
                self.skipTest(e.message)
            except ResultOrderError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except WrongDataError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except DiceNumberError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except DiceValueError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except WrongResultError as e:
                self.skipTest("Skipped. Reason: %s" % e.message)
            except TurnsNumberError as e:
                self.fail(e.message)
            except ResultError:
                pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Please specify a path to execurable file")
    exec_programm = sys.argv[1]
    if (not os.path.exists(exec_programm)
            or not os.path.isfile(exec_programm)):
        print("Wrong path to executable file has specified: %s"
              % exec_programm)
        sys.exit(1)
    TestGurgenArgs.programm = os.path.abspath(exec_programm)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGurgenArgs)
    unittest.TextTestRunner(verbosity=2).run(suite)

    TestGurgen.programm = os.path.abspath(exec_programm)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGurgen)
    unittest.TextTestRunner(verbosity=2).run(suite)
