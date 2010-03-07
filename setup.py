#!/usr/bin/env python

import os
import unittest
from setuptools import setup, find_packages

version = '0.1.4'


LONG_DESCRIPTION = '''

Version 0.1.4 Updates:
----------------------

Auto-pop functionality is now optional. New tests are now included. Additional docstrings and some other minor changes. 

QR
--

QR helps you create and work with deque, queue, and stack data structures for Redis. 

Redis is well-suited for implementations of these abstract data structures, and QR makes the work even easier in Python. QR works best for (and simplifies) the creation of bounded deques, queues, and stacks (herein, DQS's), with a defined size of elements.

This version is designed for best usage in single-writer environments. Version 0.2 will be designed for full usage in multiple-writer environments as well.

Quick Setup
-----------

You'll need Redis itself, and the current Python interface for Redis, redis-py. Put qr.py in your PYTHONPATH and you're all set.

qr.py also creates an instance of the redis-py interface object. You may already have instantiated the object in your code, so you'll want to ensure consistent namespacing. You can remove this line of code, modify the namespacing, or adjust your existing namespacing -- whatever works best for you.

Full documentation is at http://github.com/tnm/qr

'''


setup(
    name='qr',
    version=version,
    description='Create and work with Redis-backed queues, deques, stacks -- bounded and unbounded',
    long_description=LONG_DESCRIPTION,
    url='http://github.com/tnm/qr',
    author='Ted Nyman',
    author_email='tnm800@gmail.com',
    keywords='Redis, queue, data structures',
    license='MIT',
    packages=find_packages(),
    py_modules=['qr'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
	'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
   ],
)
