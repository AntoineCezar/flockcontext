from __future__ import annotations

import fcntl
from types import TracebackType
from typing import IO, Any

from timeoutcontext import timeout


class Flock:
    """Locks an opened file.

    Blocking lock:

        >>> from flockcontext import Flock
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with open(tempfile.name, "w") as fd:
        ...     with Flock(fd):
        ...         fd.write('Locked')
        6

    Blocking lock with timeout:

        >>> from flockcontext import Flock
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with open(tempfile.name, "w") as fd:
        ...     with Flock(fd, timeout=1):
        ...         fd.write('Locked')
        6

    Non blocking lock:

        >>> from flockcontext import Flock
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with open(tempfile.name, "w") as fd:
        ...     try:
        ...         with Flock(fd, blocking=False):
        ...             fd.write('Locked')
        ...     except IOError as e:
        ...         print('Can not acquire lock')
        6

    Shared lock:

        >>> from flockcontext import Flock
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with open(tempfile.name, "w") as fd:
        ...     with Flock(fd, exclusive=False):
        ...         fd.write('Locked')
        6

    Acquire and release within context:

        >>> from flockcontext import Flock
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with open(tempfile.name, "w") as fd:
        ...     with Flock(fd) as lock:
        ...         print('Lock acquired')
        ...         fd.write('Locked')
        ...         lock.release()
        ...         print('Lock released')
        ...         lock.acquire()
        ...         print('Lock acquired')
        ...         fd.write('Locked')
        Lock acquired
        6
        Lock released
        Lock acquired
        6
    """

    def __init__(
        self,
        fd: IO[Any] | int,
        exclusive: bool = True,
        blocking: bool = True,
        timeout: float | None = None,
    ) -> None:
        self._fd = fd
        self._exclusive = exclusive
        self._blocking = blocking
        self._timeout = timeout

    @property
    def _op(self) -> int:
        if self._exclusive:
            op = fcntl.LOCK_EX
        else:
            op = fcntl.LOCK_SH

        if not self._blocking:
            op = op | fcntl.LOCK_NB

        return op

    def __enter__(self) -> Flock:
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.release()

    def acquire(self) -> None:
        if self._blocking:
            with timeout(self._timeout):
                fcntl.flock(self._fd, self._op)
        else:
            fcntl.flock(self._fd, self._op)

    def release(self) -> None:
        fcntl.flock(self._fd, fcntl.LOCK_UN)
