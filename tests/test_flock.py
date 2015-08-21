#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_flock
----------------------------------

Tests for `flock` module.
"""

import unittest

from flockcontext import Flock

from .flock_testcase import FlockTestCase



class TestFlock(FlockTestCase):

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

    def test_it_can_be_released_within_context(self):
        with open(self.lockfile, 'w') as fd:
            with Flock(fd) as lock:
                lock.release()
                self.assertUnlocked(self.lockfile)

    def test_it_can_be_acquired_within_context(self):
        with open(self.lockfile, 'w') as fd:
            with Flock(fd) as lock:
                lock.release()
                lock.acquire()
                self.assertLocked(self.lockfile)


if __name__ == '__main__':
    unittest.main()
