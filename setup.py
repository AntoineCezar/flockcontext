#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'timeoutcontext',
]

test_requirements = [
]

setup(
    name='flockcontext',
    version='0.4.0',
    description="Improves fcntl.flock usage",
    long_description=readme + '\n\n' + history,
    author="Antoine Cezar",
    author_email='antoine@cezar.fr',
    url='https://github.com/AntoineCezar/flockcontext',
    packages=[
        'flockcontext',
    ],
    package_dir={'flockcontext':
                 'flockcontext'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='flock context',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
