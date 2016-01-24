# -*- coding: utf-8 -*-
import fcntl

from timeoutcontext import timeout


class Flock(object):
    """Locks an opened file.

        Blocking lock:

            >>> from flockcontext import Flock
            >>>
            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     with Flock(fd):
            >>>         lock.fd.write('Locked\n')

        Blocking lock with timeout:

            >>> from flockcontext import Flock
            >>>
            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     with Flock(fd, timeout=1):
            >>>         lock.fd.write('Locked\n')

        Non blocking lock:

            >>> from flockcontext import Flock
            >>>
            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     try:
            >>>         with Flock(fd, blocking=False):
            >>>             lock.fd.write('Locked\n')
            >>>     except IOError as e:
            >>>         print('Can not acquire lock')

        Shared lock:

            >>> from flockcontext import Flock
            >>>
            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     with Flock(fd, exclusive=False):
            >>>         lock.fd.write('Locked\n')

        Acquire and release within context:

            >>> from flockcontext import Flock
            >>>
            >>> with open('/tmp/my.lock', 'w') as fd:
            >>>     with Flock(fd) as lock:
            >>>         print('Lock acquired')
            >>>         fd.write('Locked\n')
            >>>
            >>>         lock.release()
            >>>         print('Lock released')
            >>>
            >>>         lock.acquire()
            >>>         print('Lock acquired')
            >>>         fd.write('Locked\n')
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
