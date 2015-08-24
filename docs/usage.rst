=====
Usage
=====

flockcontext provide two context manager for `fcntl.flock`_.
``Flock`` locks an opened file while ``FlockOpen`` does the same job but opens
the file for you.

.. _`fcntl.flock`: https://docs.python.org/library/fcntl.html#fcntl.flock

FlockOpen exemples
------------------

Exclusive blocking lock:: python

    from flockcontext import FlockOpen

    with FlockOpen('/tmp/my.lock', 'w') as lock:
        lock.fd.write('Locked\n')

Exclusive non-blocking lock:: python

    from flockcontext import FlockOpen

    try:
        with FlockOpen('/tmp/my.lock', 'w', blocking=False) as lock:
            lock.fd.write('Locked\n')
    except IOError as e:
        print('Can not acquire lock')

Shared blocking lock:: python

    from flockcontext import Flock

    with FlockOpen('/tmp/my.lock', 'w', exclusive=False) as lock:
        lock.fd.write('Locked\n')

Acquire and release within context:: python

    from flockcontext import FlockOpen

    with FlockOpen('/tmp/my.lock', 'w') as lock:
        print('Lock acquired')
        lock.fd.write('Locked\n')

        lock.release()
        print('Lock released')

        lock.acquire()
        print('Lock acquired')
        lock.fd.write('Locked\n')

Flock exemples
--------------

Blocking lock:: python

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        with Flock(fd):
            fd.write('Locked\n')

Non blocking lock:: python

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        try:
            with Flock(fd, blocking=False):
                fd.write('Locked\n')
        except IOError as e:
            print('Can not acquire lock')

Shared lock:: python

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        with Flock(fd, exclusive=False):
            fd.write('Locked\n')

Acquire and release within context:: python

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        with Flock(fd) as lock:
            print('Lock acquired')
            fd.write('Locked\n')

            lock.release()
            print('Lock released')

            lock.acquire()
            print('Lock acquired')
            fd.write('Locked\n')
