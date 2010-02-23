#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.1.1'

LONG_DESCRIPTION = '''

QR
--
Create and interact with Redis-based queues in Python

QR makes it easy to create and work with queue data structures for Redis. Redis is particularly suited for use as a queue, and QR makes it simple to implement one in Python. QR works best for (and simplifies) the creation of bounded queues: queues with a defined size of elements.

Quick Setup
-----------

You'll need Redis (http://code.google.com/p/redis) itself, and the current Python interface for Redis, redis-py (http://github.com/andymccurdy/redis-py).

Full documentation is in README.md or at http://github.com/tnm/qr

'''


setup(
    name='qr',
    version=version,
    description='Create and interact with Redis-based queues in Python',
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
        'Programming Language :: Python',
   ],
)
