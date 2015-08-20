===============================
Flockcontext
===============================

.. image:: https://img.shields.io/travis/AntoineCezar/flockcontext.svg
        :target: https://travis-ci.org/AntoineCezar/flockcontext

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
        :target: http://flockcontext.readthedocs.org/

.. image:: https://coveralls.io/repos/AntoineCezar/flockcontext/badge.svg?branch=master&service=github
         :target: https://coveralls.io/github/AntoineCezar/flockcontext?branch=master

.. image:: https://img.shields.io/pypi/v/flockcontext.svg
        :target: https://pypi.python.org/pypi/flockcontext


Improves `fcntl.flock <https://docs.python.org/library/fcntl.html#fcntl.flock>`_ usage.

``flock`` is a Unix command for `file locking <https://en.wikipedia.org/wiki/File_locking>`_,
the mecanism that controls access restrictions of files.

Features
--------

* Flock as a context manager

::

    from flockcontext import Flock

    with open('/tmp/my.lock', 'w') as fd:
        with Flock(fd):
            pass # Do something

Todo
----

* Avoid manual opening of files in common cases

License
-------

* Free software: BSD license
