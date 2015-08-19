# -*- coding: utf-8 -*-
import fcntl


class Flock(object):
    """Locks an opened file.

        Blocking lock exemple:

            >>> from flockcontext import Flock

            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     with Flock(fd):
            >>>         pass # Do something

        Non blocking lock exemple:

            >>> from flockcontext import Flock

            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     try:
            >>>         with Flock(fd, blocking=False):
            >>>             pass  # Do something
            >>>     except IOError as e:
            >>>         pass  # Do something else

        Shared lock exemple:

            >>> from flockcontext import Flock

            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     with Flock(fd, exclusive=False):
            >>>         pass # Do something
    """

    def __init__(self, fd, exclusive=True, blocking=True):
        self._fd = fd

        if exclusive:
            self._op = fcntl.LOCK_EX
        else:
            self._op = fcntl.LOCK_SH

        if not blocking:
            self._op = self._op | fcntl.LOCK_NB

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.release()

    def acquire(self):
        fcntl.flock(self._fd, self._op)

    def release(self):
        fcntl.flock(self._fd, fcntl.LOCK_UN)
