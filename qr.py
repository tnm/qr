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

# This is a complete nod to hotqueue -- this is one of the
# things that they did right. Natively pickling and unpiclking
# objects is pretty useful.
try:
    import cPickle as pickle
except ImportError:
    import pickle

# redis interface
redis = redis.Redis()

class NullHandler(logging.Handler):
    """A logging handler that discards all logging records"""
    def emit(self, record):
        pass

# Clients can add handlers if they are interested.
log = logging.getLogger('qr')
log.addHandler(NullHandler())

class BaseQueue(object):
    def __init__(self, key):
        self.serializer = pickle
        self.key = key
    
    def __len__(self):
        """Return the length of the queue"""
        return redis.llen(self.key)
    
    def __getitem__(self, val):
        """Get a slice or a particular index."""
        try:
            return redis.lrange(self.key, val.start, val.stop)
        except AttributeError:
            return redis.lindex(self.key, val)
        except Exception as e:
            log.error('Get item failed ** %s' % repr(e))
            return []
    
    def _pack(self, val):
        """Prepares a message to go into Redis"""
        return self.serializer.dumps(val)
    
    def _unpack(self, val):
        """Unpacks a message stored in Redis"""
        return self.serializer.loads(val)

    def extend(self, *vals):
        """Extends the elements in the queue."""
        for val in vals:
            redis.lpush(self._pack(val))

    def peek(self):
        """Look at the next item in the queue"""
        return self[-1]

    def elements(self):
        """Return all elements as a Python list"""
        return redis.lrange(self.key, 0, -1)
    
    def elements_as_json(self):
        """Return all elements as JSON object"""
        all_elements = redis.lrange(self.key, 0, -1)
        return json.dumps(all_elements)

class Deque(BaseQueue):
    """Implements a double-ended queue"""

    def push_back(self, element):
        """Push an element to the back of the deque"""
        redis.lpush(self.key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))
        
    def push_front(self, element):
        """Push an element to the front of the deque"""
        key = self.key
        push_it = redis.rpush(key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))

    def pop_front(self):
        """Pop an element from the front of the deque"""
        popped = redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped )

    def pop_back(self):
        """Pop an element from the back of the deque"""
        popped = redis.lpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)

class Queue(BaseQueue): 
    """Implements a FIFO queue"""
    
    def push(self, element):
        """Push an element"""
        redis.lpush(self.key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))

    def pop(self):
        """Pop an element"""
        popped = redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)
    
class CappedCollection(BaseQueue):
    """
    Implements a capped collection (the collection never
    gets larger than the specified size).
    """

    def __init__(self, key, size):
        BaseQueue.__init__(self, key)
        self.size = size

    def push(self, element):
        size = self.size
        pipe = redis.pipeline() # Use multi-exec command via redis-py pipelining
        pipe = pipe.lpush(self.key, self._pack(element)).ltrim(self.key, 0, size-1) # ltrim is zero-indexed 
        pipe.execute()

    def pop(self):
        popped = redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)

class Stack(BaseQueue):
    """Implements a LIFO stack""" 

    def push(self, element):
        """Push an element"""
        redis.lpush(self.key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))
         
    def pop(self):
        """Pop an element"""
        popped = redis.lpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)
    