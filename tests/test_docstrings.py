import unittest
import doctest
from flockcontext import flock
from flockcontext import flock_open


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(flock))
    tests.addTests(doctest.DocTestSuite(flock_open))
    return tests
