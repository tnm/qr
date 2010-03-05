#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.1.3'

LONG_DESCRIPTION = '''

QR
--

QR helps you create and work with deque, queue, and stack data structures for Redis. 

Redis is well-suited for implementations of these abstract data structures, and QR makes the work even easier in Python. QR works best for (and simplifies) the creation of bounded deques, queues, and stacks (herein, DQS's), with a defined size of elements.

Quick Setup
-----------

You'll need Redis itself, and the current Python interface for Redis, redis-py. Put qr.py in your PYTHONPATH and you're all set.

qr.py also creates an instance of the redis-py interface object. You may already have instantiated the object in your code, so you'll want to ensure consistent namespacing. You can remove this line of code, modify the namespacing, or adjust your existing namespacing -- whatever works best for you.

Full documentation is in README.md, or at http://github.com/tnm/qr

'''


setup(
    name='qr',
    version=version,
    description='Create and interact with Redis-based data structures in Python',
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
