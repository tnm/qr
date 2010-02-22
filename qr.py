#import redis-py and Python's JSON module
import redis
try:
    import json
except ImportError:
    import simplejson as json

#The redis-py object -- modify/remove this to match with your namespacing
redis = redis.Redis()	

#The Qr object
class Qr(object):	
	
	#Key is required; specify a size to get a sized queue
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
			print 'FOR KEY: %s\nPUSHED: %s\nPOPPED: %s' % (key, element, popped)
		
		else:
			push_it = redis.lpush(key, element)
			print 'FOR KEY: %s\nPUSHED: %s' % (key, element)

		
			
	#Pop 
	def pop(self):
		key = self.key
		popped = redis.rpop(key)
		print 'FOR KEY: %s\nPOPPED: %s' %(key, popped)
	
	#Return all elements from the queue as a Python list
	def elements(self):
		key = self.key
		size = self.size
		all_elements = redis.lrange(key, 0, size)
		return all_elements
			
		
	#Return all elements from the queue as a JSON object
	def elements_as_json(self):
		key = self.key
		size = self.size
		all_elements = redis.lrange(key, 0, size)
		all_elements_as_json = json.dumps(all_elements)
		return all_elements_as_json





	


