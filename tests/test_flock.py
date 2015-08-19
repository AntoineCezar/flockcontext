#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_flock
----------------------------------

Tests for `flock` module.
"""

import unittest
import fcntl
import os
import tempfile

from flockcontext import Flock


LOCK_EX_NB = fcntl.LOCK_EX | fcntl.LOCK_NB


class TestFlock(unittest.TestCase):

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

    def exclusive_lock(self, filepath):
        fd = open(filepath, 'w')
        fcntl.flock(fd, LOCK_EX_NB)
        return fd

    def unlock(self, fd):
        fcntl.flock(fd, fcntl.LOCK_UN)

    def test_file_is_locked_within_context(self):
        with open(self.lockfile, 'w') as fd:
            with Flock(fd) as lock:
                self.assertLocked(self.lockfile)

    def test_file_is_unlocked_after_context(self):
        with open(self.lockfile, 'w') as fd:
            with Flock(fd) as lock:
                pass

            self.assertUnlocked(self.lockfile)

    def test_non_blocking_does_not_wait_for_lock(self):
        locked_fd = self.exclusive_lock(self.lockfile)

        with self.assertRaises(IOError):
            with open(self.lockfile, 'w') as fd:
                with Flock(fd, blocking=False) as lock:
                    pass

        self.unlock(locked_fd)


if __name__ == '__main__':
    unittest.main()
