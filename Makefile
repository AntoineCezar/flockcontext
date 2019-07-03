.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "coverage-html - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "develop - link the package into the active Python's site-packages"
	@echo "install - install the package into the active Python's site-packages"

clean: clean-build clean-pyc clean-test clean-coverage

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/

clean-coverage:
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 flockcontext tests

test:
	python setup.py test

test-all: test-py27 test-py33 test-py34 test-py35 test-py36 test-py37

test-py27:
	./docker-test.sh python:2.7

test-py33:
	./docker-test.sh python:3.3

test-py34:
	./docker-test.sh python:3.4

test-py35:
	./docker-test.sh python:3.5

test-py36:
	./docker-test.sh python:3.6

test-py37:
	./docker-test.sh python:3.7

coverage: .coverage
	coverage report -m

coverage-html: .coverage
	coverage html
	open htmlcov/index.html

.coverage:  clean-coverage
	coverage run --source flockcontext setup.py test

docs:
	rm -f docs/flockcontext.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ flockcontext
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

develop: clean
	python setup.py develop

install: clean
	python setup.py install
