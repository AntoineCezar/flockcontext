from __future__ import annotations

from types import TracebackType

from .flock import Flock


class FlockOpen:
    """Opens and locks file.

    Blocking lock exemple:

        >>> from flockcontext import FlockOpen
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with FlockOpen(tempfile.name, 'w') as lock:
        ...     lock.fd.write('Locked')
        6

    Blocking lock wih timeout exemple:

        >>> from flockcontext import FlockOpen
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with FlockOpen(tempfile.name, 'w', timeout=1) as lock:
        ...     lock.fd.write('Locked')
        6

    Non blocking lock exemple:

        >>> from flockcontext import FlockOpen
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> try:
        ...     with FlockOpen(tempfile.name, 'w', blocking=False) as lock:
        ...         lock.fd.write('Locked')
        ... except IOError as e:
        ...     print('Can not acquire lock')
        6

    Shared lock exemple:

        >>> from flockcontext import FlockOpen
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with FlockOpen(tempfile.name, 'w', exclusive=False) as lock:
        ...     lock.fd.write('Locked')
        6

    Acquire and release within context:

        >>> from flockcontext import FlockOpen
        >>> from tempfile import NamedTemporaryFile
        >>>
        >>> tempfile = NamedTemporaryFile()
        >>>
        >>> with FlockOpen(tempfile.name, 'w') as lock:
        ...     print('Lock acquired')
        ...     lock.fd.write('Locked')
        ...
        ...     lock.release()
        ...     print('Lock released')
        ...
        ...     lock.acquire()
        ...     print('Lock acquired')
        ...     lock.fd.write('Locked')
        Lock acquired
        6
        Lock released
        Lock acquired
        6
    """

    def __init__(
        self,
        filepath: str,
        mode: str,
        exclusive: bool = True,
        blocking: bool = True,
        timeout: float | None = None,
    ) -> None:
        self._filepath = filepath
        self._mode = mode
        self._exclusive = exclusive
        self._blocking = blocking
        self._timeout = timeout

    def __enter__(self) -> FlockOpen:
        self.fd = open(self._filepath, self._mode)
        self._lock = Flock(
            self.fd,
            exclusive=self._exclusive,
            blocking=self._blocking,
            timeout=self._timeout,
        )
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.release()
        self.fd.close()

    def acquire(self) -> None:
        self._lock.acquire()

    def release(self) -> None:
        self._lock.release()
