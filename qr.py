"""
QR: Redis-Based Data Structures in Python

         5 Mar 2010 | Returns work correctly for both bounded and unbounded
	 4 Mar 2010 | Pop commands now return just the value
	24 Feb 2010 | QR now has deque and stack data structures (0.1.2)
	22 Feb 2010 | First public release of QR (0.1.1)
"""

__author__ = 'Ted Nyman'
__version__ = '0.1.3'
__license__ = 'MIT'

import redis

try:
    import json
except ImportError:
    import simplejson as json

#The redis-py object -- modify/remove this to match with your namespacing
redis = redis.Redis()
	
#The Deque
class Deque(object):

	#Key is required; specify a size to get a bounded deque
	def __init__(self, key, size=None):
		self.key = key
		self.size = size		

	#Push to Back
	def pushback(self, element):
		key = self.key
		length = redis.llen(key)

		if length == self.size:
			popped = redis.rpop(key)
			push_it = redis.lpush(key, element)
			print 'PUSHED: %s' % (element)
			return popped 
		
		else:
			push_it = redis.lpush(key, element)
			print 'PUSHED: %s' % (element)
		
	#Push to Front
	def pushfront(self, element):
		key = self.key
		length = redis.llen(key)

		if length == self.size:
			popped = redis.lpop(key)
			push_it = redis.rpush(key, element)
			print 'PUSHED: %s' % (element)
			return popped 
		
		else:
			push_it = redis.rpush(key, element)
			print 'PUSHED: %s' % (element)

	#Pop Front Element
	def popfront(self):
		key = self.key
		popped = redis.rpop(key)
		return popped 


	#Pop Back Element
	def popback(self):
		key = self.key
		popped = redis.lpop(key)
		return popped 


	#Return all elements from the deque as a Python list
	def elements(self):
		key = self.key
		length = redis.llen(key)
		all_elements = redis.lrange(key, 0, length)
		return all_elements
				
	#Return all elements from the deque as a JSON object
	def elements_as_json(self):
		key = self.key
		size = self.size
		length = redis.llen(key)
		all_elements = redis.lrange(key, 0, length)
		all_elements_as_json = json.dumps(all_elements)
		return all_elements_as_json

#The Queue
class Queue(object):	
	
	#Key is required; specify a size to get a bounded queue
	def __init__(self, key, size=None):
		self.key = key
		self.size = size		

	#Push
	def push(self, element):
		key = self.key
		length = redis.llen(key)

		if length == self.size:
			popped = redis.rpop(key)
			push_it = redis.lpush(key, element)
			print 'PUSHED: %s' % (element)
			return popped 
		
		else:
			push_it = redis.lpush(key, element)
			print 'PUSHED: %s' % (element)
		
	#Pop 
	def pop(self):
		key = self.key
		popped = redis.rpop(key)
		return popped 	

	#Return all elements from the queue as a Python list
	def elements(self):
		key = self.key
		length = redis.llen(key)
		all_elements = redis.lrange(key, 0, length)
		return all_elements
				
	#Return all elements from the queue as a JSON object
	def elements_as_json(self):
		key = self.key
		length = redis.llen(key)
		all_elements = redis.lrange(key, 0, length)
		all_elements_as_json = json.dumps(all_elements)
		return all_elements_as_json

#The Stack
class Stack(object):

	#Key is required; specify a size to get a bounded stack
	def __init__(self, key, size=None):
		self.key = key
		self.size = size		

	#Push
	def push(self, element):
		key = self.key
		length = redis.llen(key)

		if length == self.size:
			popped = redis.lpop(key)
			push_it = redis.lpush(key, element)
			print 'PUSHED: %s' % (element)
			return popped 
		
		else:
			push_it = redis.lpush(key, element)
			print 'PUSHED: %s' % (element)
		
	#Pop 
	def pop(self):
		key = self.key
		popped = redis.lpop(key)
		return popped 
	
	#Return all elements as a Python list
	def elements(self):
		key = self.key
		length = redis.llen(key)
		all_elements = redis.lrange(key, 0, length)
		return all_elements
					
	#Return all elements as a JSON object
	def elements_as_json(self):
		key = self.key
		length = redis.llen(key)
		all_elements = redis.lrange(key, 0, length)
		all_elements_as_json = json.dumps(all_elements)
		return all_elements_as_json
