#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

from flockcontext import FlockOpen

from .flock_testcase import FlockTestCase

try:
    TextIOWrapper = file
except NameError:
    from io import TextIOWrapper


class TestFlockOpen(FlockTestCase):

    def test_it_as_a_file_descriptor_object(self):
        with FlockOpen(self.lockfile_path, 'w') as lock:
            self.assertIsInstance(lock.fd, TextIOWrapper)

    def test_it_can_be_unlocked_within_context(self):
        with FlockOpen(self.lockfile_path, 'w') as lock:
            lock.release()
            self.assertUnlocked(self.lockfile_path)

    def test_it_can_be_acquired_within_context(self):
        with FlockOpen(self.lockfile_path, 'w') as lock:
            lock.release()
            lock.acquire()
            self.assertLocked(self.lockfile_path)
