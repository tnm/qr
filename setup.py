#!/usr/bin/env python

import os
import unittest
from setuptools import setup, find_packages

version = '0.2.0'


LONG_DESCRIPTION = '''

Full documentation (with example code) is at http://github.com/tnm/qr

QR
=====

**QR** helps you create and work with **queue, capped collection (bounded queue), 
deque, and stack** data structures for **Redis**. Redis is well-suited for 
implementations of these abstract data structures, and QR makes it even easier to 
work with the structures in Python.

Quick Setup
------------
You'll need [Redis](http://github.com/antirez/redis/ "Redis") itself (QR makes use 
of MULTI/EXEC, so you'll need the Git edge version), and the current Python interface
for Redis, [redis-py](http://github.com/andymccurdy/redis-py "redis-py"). Put **qr.py**
in your PYTHONPATH and you're all set.

**qr.py** also creates an instance of the redis-py interface object. You may already
have instantiated the object in your code, so you'll want to ensure consistent namespacing.
You can remove this line of code, modify the namespacing, or adjust your existing namespacing --
whatever works best for you.


'''


setup(
    name='qr',
    version=version,
    description='Create and work with Redis-powered queues, capped collections, deques, and stacks',
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
