QR
=====

**QR** helps you create and work with **queue, capped collection (bounded queue), deque, and stack** data structures for **Redis**. 
Redis is well-suited for implementations of these abstract data structures, and QR makes it even easier to work with the structures in Python.

Quick Setup
------------
You'll need [Redis](http://github.com/antirez/redis/ "Redis") itself -- QR makes use of MULTI/EXEC, so you'll need Redis 2.0 or 
greater (or one of the later 1.3.x releases). Also necessary is the Python interface for Redis, [redis-py](http://github.com/andymccurdy/redis-py "redis-py"). You can install QR with the included setup.py.

Basics of QR
------------------

You probably know this already, but here's the 20-second overview of these four data structures.

A **queue**:

* You push elements to the back of the queue and pop elements from the front.
* With respect to the elements, it's first in, first out (FIFO).

A **capped collection**:

* Another name for (what is essentially) a bounded queue.
* You push elements to the back, and once a maximum collection size is reached, the oldest element(s) is trimmed.

A **deque**, or double-ended queue:

* You can push values to the front *or* back of a deque, and pop elements from the front *or* back of the deque. 

A **stack**, or, as they say in German, a 'Stapelspeicher':

* You can push elements to the back of the stack and pop elements from the back of the stack.
* It's last in, first out (LIFO).

Create a QCDS 
-------------------------------------

**qr.py** includes four little classes: **Queue**, **CappedCollection**, **Deque**, and **Stack**. To create a new QCDS, just create an instance as follows:

* A first-position **key** argument is required for all objects. It's the Redis **key** you want to be associated with the QCDS.
* A second-position **size** argument is required for **CappedCollection**. That's how big you want to let the collection get.

A Queue
--------

Cool, let's create a Beatles queue, circa 1962. 

	>> from qr import Queue
	>> bqueue = Queue('Beatles')

You are now the owner of a Queue object (`bqueue`), associated with the Redis key 'Beatles'. 

    >> bqueue.push('Pete')
	>> bqueue.push('John')
    >> bqueue.push('Paul')
    >> bqueue.push('George')

Unfortunately, George Martin doesn't like Pete Best, so it's time to pop him. Since Pete was first in, and this is a queue, after all, we 
just do this:

    >> bqueue.pop()
    'Pete'

And, of course, we know who joins the band next.

    >> bqueue.push('Ringo')

We can get back (no pun intended) the elements from the queue, too. In fact, each class in QR includes two return-style methods: **elements** and **elements_as_json**. 

* Call **elements()**, and you'll get back a Python list. 

* Call **elements_as_json()**, and you'll get back the list as a JSON object.

For example:

	>> bqueue.elements()
	['Ringo', 'George', 'Paul', 'John']

	>> bqueue.elements_as_json()
	'['Ringo', 'George', 'Paul', 'John']'

A Capped Collection
--------------------

I don't know if you've heard, but Donald Knuth will be joining Radiohead soon. They need an organ player. Amazing, I know. Anyway, Radiohead has a max of five members, so someone is going to have to get kicked out of the band. Let's demonstrate this with a Capped Collection.

	>> from qr import CappedCollection
	>> radiohead_cc = CappedCollection('Radiohead', 5)

    >> radiohead_cc.push('Ed')
    >> radiohead_cc.push('Colin')
    >> radiohead_cc.push('Thom')
    >> radiohead_cc.push('Jonny')
    >> radiohead_cc.push('Phil')

    >> radiohead_cc.elements()
	['Phil', 'Jonny', 'Thom', 'Colin', 'Ed']

Now it's time for Donald to join the group.

    >> radiohead_cc.push('Donald')

And our new Radiohead is :

    >> radiohead_cc.elements()
	['Donald', 'Phil', 'Jonny', 'Thom', 'Colin']


A Deque
--------

If you wanted a deque for the Rolling Stones:

	>> from qr import Deque
	>> stones_deque = Deque('Stones')

The deque, of course, has different methods:

* pushfront()
* pushback()
* popfront()
* popback()
    

A Stack
--------

The Kinks stack is as easy as:

	>> from qr import Stack
	>> kinks_stack = Stack('Kinks')

The stack has the same methods as the queue.


Additions, More
-----------------------

Feel free to fork! 

Thanks to mafr for some initial tests. 

Author: Ted Nyman | @tnm


MIT License
------------

Copyright (c) 2010 Ted Nyman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
