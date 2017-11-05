#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import os

from setuptools import find_packages, setup

from debug_toolbar_alchemy import __author__, __version__


def read(fname):
    p = os.path.join(os.path.dirname(__file__), fname)
    with open(p, 'rb') as fid:
        return fid.read().decode('utf-8')


authors = read('AUTHORS.rst')
history = read('HISTORY.rst').replace('.. :changelog:', '')
licence = read('LICENSE.rst')
readme = read('README.rst')

requirements = read('requirements.txt').splitlines() + [
    'setuptools',
]

test_requirements = (
    read('requirements.txt').splitlines() +
    read('requirements-dev.txt').splitlines()[1:]
)

setup(
    name='django-debug-toolbar-alchemy',
    version=__version__,
    author=__author__,
    description='Django Debug Toolbar panel for SQLAlchemy.',
    long_description='\n\n'.join([readme, history, authors, licence]),
    url='https://github.com/miki725/django-debug-toolbar-alchemy',
    license='MIT',
    packages=find_packages(exclude=[]),
    install_requires=requirements,
    test_suite='tests',
    tests_require=test_requirements,
    keywords=' '.join([
        'django',
        'django-debug-toolbar',
        'sqlalchemy',
    ]),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
    ],
)
