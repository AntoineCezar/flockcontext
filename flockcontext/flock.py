# -*- coding: utf-8 -*-
import fcntl

from timeoutcontext import timeout


class Flock(object):
    """Locks an opened file.

        Blocking lock:

            >>> from flockcontext import Flock
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> with NamedTemporaryFile() as fd:
            ...     with Flock(fd):
            ...         fd.write('Locked')

        Blocking lock with timeout:

            >>> from flockcontext import Flock
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> with NamedTemporaryFile() as fd:
            ...     with Flock(fd, timeout=1):
            ...         fd.write('Locked')

        Non blocking lock:

            >>> from flockcontext import Flock
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> with NamedTemporaryFile() as fd:
            ...     try:
            ...         with Flock(fd, blocking=False):
            ...             fd.write('Locked')
            ...     except IOError as e:
            ...         print('Can not acquire lock')

        Shared lock:

            >>> from flockcontext import Flock
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> with NamedTemporaryFile() as fd:
            ...     with Flock(fd, exclusive=False):
            ...         fd.write('Locked')

        Acquire and release within context:

            >>> from flockcontext import Flock
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> with NamedTemporaryFile() as fd:
            ...     with Flock(fd) as lock:
            ...         print('Lock acquired')
            ...         fd.write('Locked')
            ...         lock.release()
            ...         print('Lock released')
            ...         lock.acquire()
            ...         print('Lock acquired')
            ...         fd.write('Locked')
            Lock acquired
            Lock released
            Lock acquired
    """

    def __init__(self, fd, exclusive=True, blocking=True, timeout=None):
        self._fd = fd
        self._exclusive = exclusive
        self._blocking = blocking
        self._timeout = timeout

    @property
    def _op(self):
        if self._exclusive:
            op = fcntl.LOCK_EX
        else:
            op = fcntl.LOCK_SH

        if not self._blocking:
            op = op | fcntl.LOCK_NB

        return op

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.release()

    def acquire(self):
        if self._blocking:
            with timeout(self._timeout):
                fcntl.flock(self._fd, self._op)
        else:
                fcntl.flock(self._fd, self._op)

    def release(self):
        fcntl.flock(self._fd, fcntl.LOCK_UN)
