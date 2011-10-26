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

class NullHandler(logging.Handler):
    """A logging handler that discards all logging records"""
    def emit(self, record):
        pass

# Clients can add handlers if they are interested.
log = logging.getLogger('qr')
log.addHandler(NullHandler())

# A dictionary of connection pools, based on the parameters used
# when connecting. This is so we don't have an unwieldy number of
# connections
connectionPools = {}

def getRedis(**kwargs):
    """Match up the provided kwargs with an existing connection pool.
    In cases where you may want a lot of queues, the redis library will
    by default open at least one connection for each. This uses redis'
    connection pool mechanism to keep the number of open file descriptors
    tractable."""
    key = ':'.join((repr(key) + '=>' + repr(value)) for key, value in kwargs.items())
    try:
        return redis.Redis(connection_pool=connectionPools[key])
    except KeyError:
        cp = redis.ConnectionPool(**kwargs)
        connectionPools[key] = cp
        return redis.Redis(connection_pool=cp)

class BaseQueue(object):
    """Base functionality common to queues"""
    @staticmethod
    def all(t, pattern, **kwargs):
        r = getRedis(**kwargs)
        return [t(k, **kwargs) for k in r.keys(pattern)]
    
    def __init__(self, key, **kwargs):
        self.serializer = pickle
        self.redis = getRedis(**kwargs)
        self.key = key
    
    def __len__(self):
        """Return the length of the queue"""
        return self.redis.llen(self.key)
    
    def __getitem__(self, val):
        """Get a slice or a particular index."""
        try:
            return [self._unpack(i) for i in self.redis.lrange(self.key, val.start, val.stop)]
        except AttributeError:
            return self._unpack(self.redis.lindex(self.key, val))
        except Exception as e:
            log.error('Get item failed ** %s' % repr(e))
            return None
    
    def _pack(self, val):
        """Prepares a message to go into Redis"""
        return self.serializer.dumps(val)
    
    def _unpack(self, val):
        """Unpacks a message stored in Redis"""
        try:
            return self.serializer.loads(val)
        except TypeError:
            return None
    
    def dump(self, fobj):
        """Destructively dump the contents of the queue into fp"""
        next = self.redis.rpop(self.key)
        while next:
            fobj.write(next)
            next = self.redis.rpop(self.key)
    
    def load(self, fobj):
        """Load the contents of the provided fobj into the queue"""
        next = self.serializer.load(obj)
        while next:
            self.redis.lpush(self.serializer._pack(next))
            next = self.serializer.load(fobj)
    
    def dumpfname(self, fname, truncate=False):
        """Destructively dump the contents of the queue into fname"""
        if truncate:
            with file(fname, 'w+') as f:
                self.dump(f)
        else:
            with file(fname, 'a+') as f:
                self.dump(f)
    
    def loadfname(self, fname):
        """Load the contents of the contents of fname into the queue"""
        with file(fname) as f:
            self.load(f)
    
    def extend(self, vals):
        """Extends the elements in the queue."""
        with self.redis.pipeline(transaction=False) as pipe:
            for val in vals:
                pipe.lpush(self.key, self._pack(val))
            pipe.execute()
    
    def peek(self):
        """Look at the next item in the queue"""
        return self[-1]

    def elements(self):
        """Return all elements as a Python list"""
        return self.redis.lrange(self.key, 0, -1)
    
    def elements_as_json(self):
        """Return all elements as JSON object"""
        all_elements = self.redis.lrange(self.key, 0, -1)
        return json.dumps(all_elements)

class Deque(BaseQueue):
    """Implements a double-ended queue"""
    
    @staticmethod
    def all(pattern='*', **kwargs):
        return BaseQueue.all(Deque, pattern, **kwargs)

    def push_back(self, element):
        """Push an element to the back of the deque"""
        self.redis.lpush(self.key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))
        
    def push_front(self, element):
        """Push an element to the front of the deque"""
        key = self.key
        push_it = self.redis.rpush(key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))

    def pop_front(self):
        """Pop an element from the front of the deque"""
        popped = self.redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped )

    def pop_back(self):
        """Pop an element from the back of the deque"""
        popped = self.redis.lpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)

class Queue(BaseQueue): 
    """Implements a FIFO queue"""

    @staticmethod
    def all(pattern='*', **kwargs):
        return BaseQueue.all(Queue, pattern, **kwargs)
    
    def push(self, element):
        """Push an element"""
        self.redis.lpush(self.key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))

    def pop(self):
        """Pop an element"""
        popped = self.redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)
    
class CappedCollection(BaseQueue):
    """
    Implements a capped collection (the collection never
    gets larger than the specified size).
    """
    
    @staticmethod
    def all(pattern='*', **kwargs):
        return BaseQueue.all(CappedCollection, pattern, **kwargs)

    def __init__(self, key, size, **kwargs):
        BaseQueue.__init__(self, key, **kwargs)
        self.size = size

    def push(self, element):
        size = self.size
        with self.redis.pipeline() as pipe:
            # ltrim is zero-indexed 
            pipe = pipe.lpush(self.key, self._pack(element)).ltrim(self.key, 0, size-1)
            pipe.execute()

    def extend(self, vals):
        """Extends the elements in the queue."""
        with self.redis.pipeline() as pipe:
            for val in vals:
                pipe.lpush(self.key, self._pack(val))
            pipe.ltrim(self.key, 0, self.size-1)
            pipe.execute()

    def pop(self):
        popped = self.redis.rpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)

class Stack(BaseQueue):
    """Implements a LIFO stack""" 

    @staticmethod
    def all(pattern='*', **kwargs):
        return BaseQueue.all(Stack, pattern, **kwargs)
    
    def push(self, element):
        """Push an element"""
        self.redis.lpush(self.key, self._pack(element))
        log.debug('Pushed ** %s ** for key ** %s **' % (element, self.key))
         
    def pop(self):
        """Pop an element"""
        popped = self.redis.lpop(self.key)
        log.debug('Popped ** %s ** from key ** %s **' % (popped, self.key))
        return self._unpack(popped)
    