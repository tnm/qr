QR
=====

**QR** helps you create and work with **deque, queue, and stack** data structures for **Redis**. Redis is well-suited for implementations of these abstract data structures, and QR makes the work even easier in Python. QR works best for (and simplifies) the creation of **bounded** deques, queue, and stacks (herein, DQS's), with a defined size of elements. 


Quick Setup
------------
You'll need [Redis](http://code.google.com/p/redis/ "Redis") itself, and the current Python interface for Redis, [redis-py](http://github.com/andymccurdy/redis-py "redis-py"). Put **qr.py** in your PYTHONPATH and you're all set.

**qr.py** also creates an instance of the redis-py interface object. You may already have instantiated the object in your code, so you'll want to ensure consistent namespacing. You can remove this line of code, modify the namespacing, or adjust your existing namespacing -- whatever works best for you.


QR as Abstraction
------------------

You probably now this already, but here's the 20-second overview of these three data structures.

A **deque**, or double-ended queue:

* You can push values to the front *or* back of a deque, and pop elements from the front *or* back of the deque. 
* With respect to the elements, it's first in, first out (FIFO).

A **queue**:

* You **push** values to the back of the queue and **pop** values from the front.
* It's also FIFO.

A **stack**, or, as they say in German, a 'Stapelspeicher':

* You can push values to the back of the stack and pop values from the back of the stack.
* It's last in, first out (LIFO).

For each DQS structure, you can create two varieties:

* **Bounded**: once the DQS reaches a specified size of elements, it will pop an element.

* **Unbounded**: the DQS can grow to any size, and will not pop elements unless you explicitly ask it to.

Consider a use case like this: you may have any number of comments on a blog post, but you only want to display the most recent 10. You can use a bounded queue, and pop the older comments as new ones come in. (We'll do that exact thing in an example at the end of this README).

Create a DQS 
-------------------------------------

**qr.py** includes three classes: **Deque**, **Queue**, and, **Stack**. To create a new DQS, just create an instance as follows:

* A first-position **key** argument is required. It's the Redis key you want to be associated with the DQS.
* A second-position **size** argument is optional. Without a size argument you get an unbounded DQS. With a specified size, you get a bounded DQS.

A Queue
--------

Cool, let's create a version of The Beatles that, rather ahistorically, has just three members. Start your Redis server, and now:

	>> from qr import Queue
	>> bqueue = Queue('Beatles', 3)

You are now the owner of a Queue object ('bqueue'), associated with the Redis key 'Beatles'. The Queue object has a specified size of 3 elements. Let's push some elements:

	>> bqueue.push('Ringo')
	PUSHED: 'Ringo'

	>> bqueue.push('Paul')
	PUSHED: 'Paul'

	>> bqueue.push('John')
	PUSHED: 'John'

	>> bqueue.push('George')
	PUSHED: 'George' | POPPED: 'Ringo'

Since the queue was **capped at three elements**, the addition of 'George' resulted in a pop of the first-in element (in this case, 'Ringo'). Sorry, Ringo, you're out of the band.

You can utilize **pop** at anytime. To pop the oldest element, just do this:

	>>bqueue.pop()
	POPPED: 'Paul'

A Deque
--------

If you wanted a deque for the Beatles, you'd just do:

	>> from qr import Deque
	>> beatles_deque = Deque('Beatles', 3)

Instead of **push** and **pop**, you can use **frontpush**, **frontpop**, **backpush**, and **backpop** methods.


A Stack
--------

The Beatles stack is as easy as:

	>> from qr import Stack
	>> beatles_stack = Stack('Beatles', 3)

The stack has the same methods as the queue.


Return the Values
-----------------

Let's return some data from a DQS! Each class in QR includes two return-style methods: **elements** and **elements_as_json**. 

* Call **elements**, and you'll get back a Python list. 

* Call **elements_as_json**, and you'll get back the list as a JSON object.

For example:

	>>beatles_queue.elements()
	['John', 'George']

	#Let's bring Ringo back into the band
	>> beatles_queue.push('Ringo')
	FOR KEY: 'Beatles'
	PUSHED: 'Ringo'

	#The elements method will return the updated list
	>>beatles_queue.elements()
	['Ringo', 'John', 'George']

	>>beatles_queue.elements_as_json()
	'['Ringo', 'John', 'George']'

To-Do, Additions, More
-----------------------

Some more documentation will be added soon. I will likely implement a few more abstract data structures to make this something of a library. :)

Feel free to fork! 

Author: Ted Nyman | @tnm8

Also, A Real-World Example: Blog Comments
-----------------------------------

Imagine you have a Django view that handles blog comments. You have an arbitrary number of blog comments. You want to return only the most recent ten blog comments to your template. Skipping to the relevant parts, it's as easy as this:

	#The recent comments are represented as a queue with 10 elements
	most_recent_comments = Qr('recent_comments', 10)

	#The view has receieved a new comment from a HTML form!
	new_comment = 'No way man, La Forge was the best character!'

	#Add the comment to your comment queue. If there are already 10 comments, the oldest one gets popped.
	most_recent_comments.push(new_comment)

	#Create a list of the most recent 10 comments.
	comments_for_template = most_recent_comments.elements()

	#Now send the comments back to your template. In the template, you could loop through it and you're done.


	
MIT License
------------

Copyright (c) 2010 Ted Nyman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


	


