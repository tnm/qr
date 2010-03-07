QR
=====

**QR** helps you create and work with **deque, queue, and stack** data structures for **Redis**. Redis is well-suited for implementations of these abstract data structures, and QR makes the work even easier in Python. QR works best for (and simplifies) the creation of **bounded** deques, queues, and stacks (herein, DQS's), with a defined size of elements. 

Version 0.1 is designed for simple, single-writer operations. Version 0.2 will be committed soon and will allow for safety with multiple writers, as well as *peek* functionality.


Quick Setup
------------
You'll need [Redis](http://code.google.com/p/redis/ "Redis") itself, and the current Python interface for Redis, [redis-py](http://github.com/andymccurdy/redis-py "redis-py"). Put **qr.py** in your PYTHONPATH and you're all set.

**qr.py** also creates an instance of the redis-py interface object. You may already have instantiated the object in your code, so you'll want to ensure consistent namespacing. You can remove this line of code, modify the namespacing, or adjust your existing namespacing -- whatever works best for you.


QR as Abstraction
------------------

You probably know this already, but here's the 20-second overview of these three data structures.

A **deque**, or double-ended queue:

* You can push values to the front *or* back of a deque, and pop elements from the front *or* back of the deque. 
* With respect to the elements, it's first in, first out (FIFO).

A **queue**:

* You push elements to the back of the queue and pop elements from the front.
* It's also FIFO.

A **stack**, or, as they say in German, a 'Stapelspeicher':

* You can push elements to the back of the stack and pop elements from the back of the stack.
* It's last in, first out (LIFO).

For each DQS structure, you can create two varieties:

* **Bounded**: once the DQS reaches a specified size of elements, it will either:
	* Prevent the addition of new elements (auto=False)
	* Respond to push commands by popping the oldest element and pushing the newest element (auto=True)

* **Unbounded**: the DQS can grow to any size


Create a DQS 
-------------------------------------

**qr.py** includes three classes: **Deque**, **Queue**, and **Stack**. To create a new DQS, just create an instance as follows:

* A first-position **key** argument is required. It's the Redis key you want to be associated with the DQS.
* A second-position **size** argument is optional. Without a size argument you get an unbounded DQS. With a specified size, you get a bounded DQS.
* A third-position **auto** argument is optional. Set auto=True for automatic popping of oldest elements in a bounded queue; default is auto=False

Note: For non-auto-pop bounded queues at their maximum size, the element you attempt to push will simply be ignored, and the lack of a successful push will be logged. This is to maintain flexibility 
for implementations of the queue -- i.e. there is no built-in 'wait list', but you could implement one if you'd like.

A Queue
--------

Cool, let's create a version of The Beatles that, rather ahistorically, has just three members. Start your Redis server, and now:

	>> from qr import Queue
	>> bqueue = Queue('Beatles', 3, True)

You are now the owner of a Queue object ('bqueue'), associated with the Redis key 'Beatles'. The Queue object has a specified size of 3 elements, and auto-pop is set to True. Let's push some elements:

	>> bqueue.push('Ringo')
	>> bqueue.push('Paul')
	>> bqueue.push('John')
	>> bqueue.push('George')
	'Ringo'

Since the queue was **capped at three elements**, and auto-pop is set to True, the addition of 'George' resulted in a pop of the first-in element (in this case, 'Ringo'). Sorry, Ringo, you're out of the band.

You can utilize **pop** at anytime. Any pop command will return the relevant element. To pop the oldest element, just do this:

	>>bqueue.pop()
	'Paul'

A Deque
--------

If you wanted a deque for the Rolling Stones that does not automatically pop elements, you'd just do:

	>> from qr import Deque
	>> stones_deque = Deque('Stones', 3)

Instead of **push** and **pop**, you can use **pushfront**, **popfront**, **pushback**, and **popback** methods.


A Stack
--------

The Kinks stack is as easy as:

	>> from qr import Stack
	>> kinks_stack = Stack('Kinks', 3)

The stack has the same methods as the queue.


Return the Values
-----------------

Let's return some data from a DQS! Each class in QR includes two return-style methods: **elements** and **elements_as_json**. 

* Call **elements**, and you'll get back a Python list. 

* Call **elements_as_json**, and you'll get back the list as a JSON object.

For example:

	>>bqueue.elements()
	['John', 'George']

	#Let's bring Ringo back into the band
	>> bqueue.push('Ringo')

	#The elements method will return the updated list
	>>bqueue.elements()
	['Ringo', 'John', 'George']

	>>bqueue.elements_as_json()
	'['Ringo', 'John', 'George']'

To-Do, Additions, More
-----------------------

Version 0.2.0 will include classes designed for multi-writer environments.

Feel free to fork! 

Author: Ted Nyman | @tnm8


MIT License
------------

Copyright (c) 2010 Ted Nyman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
