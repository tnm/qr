"""
QR | Redis-Based Data Structures in Python

"""

__author__ = 'Ted Nyman'
__version__ = '0.3.0'
__license__ = 'MIT'

import redis
import logging

try:
    import json
except ImportError:
    import simplejson as json

# redis interface
redis = redis.Redis()

class NullHandler(logging.Handler):
    """A logging handler that discards all logging records"""
    def emit(self, record):
        pass

# Clients can add handlers if they are interested.
log = logging.getLogger('qr')
log.addHandler(NullHandler())
	
class Deque(object):
    """Implements a double-ended queue"""

    def __init__(self, key):
        self.key = key

    def push_back(self, element):
        """Push an element to the back of the deque"""
        redis.lpush(self.key, element)
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))
		
    def push_front(self, element):
        """Push an element to the front of the deque"""
        key = self.key
        push_it = redis.rpush(key, element)
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))

    def pop_front(self):
        """Pop an element from the front of the deque"""
        popped = redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return popped 

    def pop_back(self):
        """Pop an element from the back of the deque"""
        popped = redis.lpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return popped 

    def elements(self):
        """Return all elements as a Python list"""
        all_elements = redis.lrange(self.key, 0, -1)
        return all_elements
				
    def elements_as_json(self):
        """Return all elements as a JSON object"""
        all_elements = redis.lrange(self.key, 0, -1)
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json

class Queue(object):	
    """Implements a FIFO queue"""

    def __init__(self, key):
        self.key = key
	
    def push(self, element):
        """Push an element"""
        redis.lpush(self.key, element)
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))

    def pop(self):
        """Pop an element"""
        popped = redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return popped 	

    def elements(self):
        """Return all elements as a Python list"""
        all_elements = redis.lrange(self.key, 0, -1) or [ ]
        return all_elements
				
    def elements_as_json(self):
        """Return all elements as a JSON object"""	
        all_elements = redis.lrange(self.key, 0, -1) or [ ]
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json

class CappedCollection(object):
    """
    Implements a capped collection (the collection never
    gets larger than the specified size).
    """

    def __init__(self, key, size):
        self.key = key
        self.size = size

    def push(self, element):
        size = self.size
        pipe = redis.pipeline() # Use multi-exec command via redis-py pipelining
        pipe = pipe.lpush(self.key, element).ltrim(self.key, 0, size-1) # ltrim is zero-indexed 
        pipe.execute()

    def pop(self):
        popped = redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return popped

    def elements(self):
        """Return all elements as Python list"""
        all_elements = redis.lrange(self.key, 0, -1)   
        return all_elements

    def elements_as_json(self):
        """Return all elements as JSON object"""
        all_elements = redis.lrange(self.key, 0, -1)
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json

class Stack(object):
    """Implements a LIFO stack""" 

    def __init__(self, key):
        self.key = key

    def push(self, element):
        """Push an element"""
        redis.lpush(self.key, element)
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))
		 
    def pop(self):
        """Pop an element"""
        popped = redis.lpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return popped 
	
    def elements(self):
        """Return all elements as Python list"""
        all_elements = redis.lrange(self.key, 0, -1)   
        return all_elements

    def elements_as_json(self):
        """Return all elements as JSON object"""
        all_elements = redis.lrange(self.key, 0, -1)
        all_elements_as_json = json.dumps(all_elements)
        return all_elements_as_json
