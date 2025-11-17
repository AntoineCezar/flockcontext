from flockcontext import Flock

from .flock_testcase import FlockTestCase


class TestFlock(FlockTestCase):
    def test_file_is_locked_within_context(self):
        with Flock(self.lockfile_handle):
            self.assertLocked(self.lockfile_path)

    def test_file_is_unlocked_after_context(self):
        with Flock(self.lockfile_handle):
            pass

        self.assertUnlocked(self.lockfile_path)

    def test_non_blocking_does_not_wait_for_lock(self):
        self.lock(self.lockfile_path)

        with self.assertRaises(IOError):
            with Flock(self.lockfile_handle, blocking=False):
                pass

    def test_it_can_be_released_within_context(self):
        with Flock(self.lockfile_handle) as lock:
            lock.release()
            self.assertUnlocked(self.lockfile_path)

    def test_it_can_be_acquired_within_context(self):
        with Flock(self.lockfile_handle) as lock:
            lock.release()
            lock.acquire()
            self.assertLocked(self.lockfile_path)

    def test_it_raise_timeouterror_if_timeout_is_reached(self):
        self.lock(self.lockfile_path)

        with self.assertRaises(TimeoutError):
            with Flock(self.lockfile_handle, timeout=1):
                pass

    def test_timeout_is_ignored_when_not_blocking(self):
        self.lock(self.lockfile_path)

        with self.assertRaises(IOError):
            with Flock(self.lockfile_handle, blocking=False, timeout=1):
                pass
