#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
flock_testcase
----------------------------------

flockcontext base TestCase.
"""

import unittest
import fcntl
import os
import tempfile
from contextlib import contextmanager

from flockcontext import Flock

LOCK_EX_NB = fcntl.LOCK_EX | fcntl.LOCK_NB


class FlockTestCase(unittest.TestCase):

    def setUp(self):
        _, path = tempfile.mkstemp()
        self.lockfile = path
        self.addCleanup(os.remove, path)

    def assertLocked(self, filepath):
        with self.assertRaises(IOError):
            with open(filepath, 'w') as fd:
                fcntl.flock(fd, LOCK_EX_NB)

    def assertUnlocked(self, filepath):
        try:
            with open(filepath, 'w') as fd:
                fcntl.flock(fd, LOCK_EX_NB)
        except IOError:
            self.fail('%s is locked.' % lockfile)

    @contextmanager
    def exclusive_lock(self, filepath):
        fd = open(filepath, 'w')
        fcntl.flock(fd, LOCK_EX_NB)

        try:
            yield fd
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            fd.close()
