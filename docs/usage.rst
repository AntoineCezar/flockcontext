========
Usage
========

Blocking lock exemple::

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        with Flock(fd):
            pass # Do something

Non blocking lock exemple::

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        try:
            with Flock(fd, blocking=False):
                pass  # Do something
        except IOError as e:
            pass  # Do something else

Shared lock exemple::

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        with Flock(fd, exclusive=False):
            pass # Do something
