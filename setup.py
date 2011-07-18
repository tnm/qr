#!/usr/bin/env python

import os
import unittest
from setuptools import setup, find_packages

version = '0.3.0'


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
for Redis, [redis-py](http://github.com/andymccurdy/redis-py "redis-py"). 

Run setup.py to install qr.

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
