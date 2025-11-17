import fcntl
import os
import tempfile
import unittest

LOCK_EX_NB = fcntl.LOCK_EX | fcntl.LOCK_NB


class FlockTestCase(unittest.TestCase):
    def setUp(self):
        handle, path = self.mkstemp()
        self.lockfile_handle = handle
        self.lockfile_path = path

    def assertLocked(self, filepath):
        with self.assertRaises(IOError):
            with open(filepath, "w") as fd:
                fcntl.flock(fd, LOCK_EX_NB)

    def assertUnlocked(self, filepath):
        try:
            with open(filepath, "w") as fd:
                fcntl.flock(fd, LOCK_EX_NB)
        except IOError:
            self.fail("%s is locked." % filepath)

    def mkstemp(self):
        handle, path = tempfile.mkstemp()
        self.addCleanup(os.remove, path)

        return handle, path

    def lock(self, path):
        fd = self.open(path)
        fcntl.flock(fd, LOCK_EX_NB)
        self.addCleanup(fcntl.flock, fd, fcntl.LOCK_UN)

    def open(self, path, mode="r"):
        fd = open(path, mode)
        self.addCleanup(fd.close)

        return fd
