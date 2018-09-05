.PHONY: clean-pyc clean-build clean

help:  ## show help
	@grep -E '^[a-zA-Z_\-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		cut -d':' -f1- | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


install:  ## install all requirements including for testing
	pip install -U -r requirements-dev.txt

install-quite:  ## same as install but pipes all output to /dev/null
	pip install -r requirements-dev.txt > /dev/null

clean: clean-build clean-pyc  ## remove all artifacts

clean-build:  ## remove build artifacts
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

clean-pyc:  ##  remove Python file artifacts
	-@find . -name '*.pyc' -follow -print0 | xargs -0 rm -f
	-@find . -name '*.pyo' -follow -print0 | xargs -0 rm -f
	-@find . -name '__pycache__' -type d -follow -print0 | xargs -0 rm -rf

importanize:
	importanize --ci

lint:  ## check project flake8 and importanize
	flake8 .
	python --version | grep "Python 3" && make importanize || true

test:  ## run tests quickly with the default Python
	echo TODO

check: lint clean clean test  ## run all necessary steps to check validity of project

release: clean  ## package and upload a release
	python setup.py sdist bdist_wheel upload

dist: clean  ## create distribution package for testing
	python setup.py sdist bdist_wheel
	ls -l dist
