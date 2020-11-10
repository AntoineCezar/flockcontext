# -*- coding: utf-8 -*-
from .flock import Flock


class FlockOpen(object):
    """Opens and locks file.

        Blocking lock exemple:

            >>> from flockcontext import FlockOpen
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> tempfile = NamedTemporaryFile()
            >>> with FlockOpen(tempfile.name, 'w') as lock:
            ...     lock.fd.write('Locked')

        Blocking lock wih timeout exemple:

            >>> from flockcontext import FlockOpen
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> tempfile = NamedTemporaryFile()
            >>>
            >>> with FlockOpen(tempfile.name, 'w', timeout=1) as lock:
            ...     lock.fd.write('Locked')

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

        Shared lock exemple:

            >>> from flockcontext import FlockOpen
            >>> from tempfile import NamedTemporaryFile
            >>>
            >>> tempfile = NamedTemporaryFile()
            >>>
            >>> with FlockOpen(tempfile.name, 'w', exclusive=False) as lock:
            ...     lock.fd.write('Locked')

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
            Lock released
            Lock acquired
    """

    def __init__(self, filepath, mode, **flock_kwargs):
        self._filepath = filepath
        self._mode = mode
        self._flock_kwargs = flock_kwargs

    def __enter__(self):
        self.fd = open(self._filepath, self._mode)
        self._lock = Flock(self.fd, **self._flock_kwargs)
        self.acquire()
        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.release()
        self.fd.close()

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()
