"""
QR | Redis-Based Data Structures in Python

	26 Apr 2010 | Major API change; capped collections, remove autopop (0.2.0)
     7 Mar 2010 | Auto popping for bounded queues is optional (0.1.4)
     5 Mar 2010 | Returns work for both bounded and unbounded (0.1.3)
	 4 Mar 2010 | Pop commands now return just the value
	24 Feb 2010 | QR now has deque and stack data structures (0.1.2)
	22 Feb 2010 | First public release of QR (0.1.1)
"""

__author__ = 'Ted Nyman'
__version__ = '0.2.0'
__license__ = 'MIT'

import redis
import logging

try:
    import json
except ImportError:
    import simplejson as json

#The redis-py object -- modify/remove this to match with your namespacing
redis = redis.Redis()

class NullHandler(logging.Handler):
    """A logging handler that discards all logging records"""
    def emit(self, record):
        pass

#Disable logging to prevent warnings from the logging module. Clients 
#can add their own handlers if they are interested.
log = logging.getLogger('qr')
log.addHandler(NullHandler())
	
#The Data Structures
class Deque(object):
    """Implements a double-ended queue"""

    def __init__(self, key):
        self.key = key

    def pushback(self, element):
        """Push an element to the back"""
        key = self.key
        push_it = redis.lpush(key, element)
        log.debug('PUSHED: %s' % (element))
		
    def pushfront(self, element):
        """Push an element to the front"""
        key = self.key
        push_it = redis.rpush(key, element)
        log.debug('PUSHED: %s' % (element))

    def popfront(self):
        """Pop an element from the front"""
        key = self.key
        popped = redis.rpop(key)
        return popped 

    def popback(self):
        """Pop an element from the back"""
        key = self.key
        popped = redis.lpop(key)
        return popped 

    def elements(self):
        """Return all elements as a Python list"""
        key = self.key
        all_elements = redis.lrange(key, 0, -1)
        return all_elements
				
    def elements_as_json(self):
        """Return all elements as a JSON object"""
        key = self.key
        all_elements = redis.lrange(key, 0, -1)
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json

class Queue(object):	
    """Implements a FILO queue"""

    def __init__(self, key):
        self.key = key
	
    def push(self, element):
        """Push an element"""
        key = self.key
        push_it = redis.lpush(key, element)
        log.debug('PUSHED: %s' % (element))
		
    def pop(self):
        """Pop an element"""
        key = self.key
        popped = redis.rpop(key)
        return popped 	

    def elements(self):
        """Return all elements as a Python list"""
        key = self.key
        all_elements = redis.lrange(key, 0, -1) or [ ]
        return all_elements
				
    def elements_as_json(self):
        """Return all elements as a JSON object"""	
        key = self.key
        all_elements = redis.lrange(key, 0, -1) or [ ]
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json

class CappedCollection(object):
    """Implements a capped collection (the collection never
    gets larger than the specified size)."""

    def __init__(self, key, size):
        self.key = key
        self.size = size

    def push(self, element):
        key = self.key
        size = self.size
        pipe = redis.pipeline() #Use multi-exec command via redis-py pipelining
        pipe = pipe.lpush(key, element).ltrim(key, 0, size-1) #ltrim is zero-indexed 
        pipe.execute()

    def pop(self):
        key = self.key
        size = self.size
        popped = redis.rpop(key)
        return popped

    def elements(self):
        """Return all elements as Python list"""
        key = self.key
        all_elements = redis.lrange(key, 0, -1)   
        return all_elements

    def elements_as_json(self):
        """Return all elements as JSON object"""
        key = self.key
        all_elements = redis.lrange(key, 0, -1)
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json

class Stack(object):
    """Implements a LIFO stack""" 

    def __init__(self, key):
        self.key = key

    def push(self, element):
        """Push an element"""
        key = self.key
        push_it = redis.lpush(key, element)
        log.debug('PUSHED: %s' % (element))
		 
    def pop(self):
        """Pop an element"""
        key = self.key
        popped = redis.lpop(key)
        return popped 
	
    def elements(self):
        """Return all elements as Python list"""
        key = self.key
        all_elements = redis.lrange(key, 0, -1)   
        return all_elements

    def elements_as_json(self):
        """Return all elements as JSON object"""
        key = self.key
        all_elements = redis.lrange(key, 0, -1)
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json
