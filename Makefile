.PHONY: clean-pyc clean-build docs clean

help:
	@echo "install - install all requirements including for testing"
	@echo "install-quite - same as install but pipes all output to /dev/null"
	@echo "clean - remove all artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "check - run all necessary steps to check validity of project"
	@echo "release - package and upload a release"
	@echo "dist - package"

install:
	pip install -U -r requirements-dev.txt

install-quite:
	pip install -r requirements-dev.txt > /dev/null

clean: clean-build clean-pyc

clean-build:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

clean-pyc:
	-@find . -name '*.pyc' -follow -print0 | xargs -0 rm -f
	-@find . -name '*.pyo' -follow -print0 | xargs -0 rm -f
	-@find . -name '__pycache__' -type d -follow -print0 | xargs -0 rm -rf

importanize:
	importanize --ci

lint:
	flake8 .
	python --version | grep "Python 3" && make importanize || true

test:
	echo TODO

check: lint clean-build clean-pyc test

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
