import os
import qr
import redis
import unittest

r = redis.Redis()

class Queue(unittest.TestCase):
    def setUp(self):
        r.delete('qrtestqueue')
        self.q = qr.Queue(key='qrtestqueue')
        self.assertEquals(len(self.q), 0)

    def test_roundtrip(self):
        q = self.q
        q.push('foo')
        self.assertEquals(len(q), 1)
        self.assertEquals(q.pop(), 'foo')
        self.assertEquals(len(q), 0)

    def test_order(self):
        q = self.q
        q.push('foo')
        q.push('bar')
        self.assertEquals(q.pop(), 'foo')
        self.assertEquals(q.pop(), 'bar')

    def test_order_mixed(self):
        q = self.q
        q.push('foo')
        self.assertEquals(q.pop(), 'foo')
        q.push('bar')
        self.assertEquals(q.pop(), 'bar')

    def test_len(self):
        count = 100
        for i in range(count):
            self.assertEquals(len(self.q), i)
            self.q.push(i)
        for i in range(count):
            self.assertEquals(len(self.q), count - i)
            self.q.pop()
        self.q.clear()

    def test_get_item(self):
        count = 100
        items = [i for i in range(count)]
        self.q.clear()
        self.q.extend(items)
        items.reverse()
        # Get single values
        for i in range(count):
            self.assertEquals(self.q[i], items[i])
        # Get small ranges
        for i in range(count-1):
            self.assertEquals(self.q[i:i+1], items[i:i+1])
        # Now get the whole range
        self.assertEquals(self.q[0:-1], items[0:-1])
        self.q.clear()
    
    def test_extend(self):
        '''Test extending a queue, including with a generator'''
        count = 100
        self.q.extend(i for i in range(count))
        self.assertEquals(len(self.q), count)
        self.q.clear()
        
        self.q.extend([i for i in range(count)])
        self.assertEquals(len(self.q), count)
        self.q.clear()
        
        self.q.extend(range(count))
        self.assertEquals(self.q.elements(), [count - i - 1 for i in range(count)])
        self.q.clear()
            
    def test_pack_unpack(self):
        '''Make sure that it behaves like python-object-in, python-object-out'''
        count = 100
        self.q.extend({'key': i} for i in range(count))
        next = self.q.pop()
        while next:
            self.assertTrue(isinstance(next, dict))
            next = self.q.pop()
    
    def test_dump_load(self):
        # Get a temporary file to dump a queue to that file
        count = 100
        self.q.extend(range(count))
        self.assertEquals(self.q.elements(), [count - i - 1for i in range(count)])
        with os.tmpfile() as f:
            self.q.dump(f)
            # Now, assert that it is empty
            self.assertEquals(len(self.q), 0)
            # Now, try to load it back in
            f.seek(0)
            self.q.load(f)
            self.assertEquals(len(self.q), count)
            self.assertEquals(self.q.elements(), [count - i - 1 for i in range(count)])
            # Now clean up after myself
            f.truncate()
            self.q.clear()
    
class CappedCollection(unittest.TestCase):
    def setUp(self):
        r.delete('qrtestcc')
        self.aq = qr.CappedCollection(key='qrtestcc', size=3)
        self.assertEquals(len(self.aq), 0)

    def test_roundtrip(self):
        aq = self.aq
        aq.push('foo')
        self.assertEquals(len(aq), 1)
        self.assertEquals(aq.pop(), 'foo')
        self.assertEquals(len(aq), 0)

    def test_order(self):
        aq = self.aq
        aq.push('foo')
        aq.push('bar')
        self.assertEquals(aq.pop(), 'foo')
        self.assertEquals(aq.pop(), 'bar')

    def test_order_mixed(self):
        aq = self.aq
        aq.push('foo')
        self.assertEquals(aq.pop(), 'foo')
        aq.push('bar')
        self.assertEquals(aq.pop(), 'bar')

    def test_limit(self):
        aq = self.aq
        aq.push('a')
        aq.push('b')
        aq.push('c')
        self.assertEquals(len(aq), 3)
        aq.push('d')
        aq.push('e')
        self.assertEquals(len(aq), 3)
        self.assertEquals(aq.pop(), 'c')
        self.assertEquals(aq.pop(), 'd')
        self.assertEquals(aq.pop(), 'e')
        self.assertEquals(len(aq), 0)

    def test_extend(self):
        '''Test extending a queue, including with a generator'''
        count = 100
        self.aq.extend(i for i in range(count))
        self.assertEquals(len(self.aq), self.aq.size)
        self.aq.clear()

class Stack(unittest.TestCase):
    def setUp(self):
        r.delete('qrteststack')
        self.stack = qr.Stack(key='qrteststack')

    def test_roundtrip(self):
        stack = self.stack
        stack.push('foo')
        self.assertEquals(len(stack), 1)
        self.assertEquals(stack.pop(), 'foo')
        self.assertEquals(len(stack), 0)

    def test_order(self):
        stack = self.stack
        stack.push('foo')
        stack.push('bar')
        self.assertEquals(stack.pop(), 'bar')
        self.assertEquals(stack.pop(), 'foo')

    def test_order_mixed(self):
        stack = self.stack
        stack.push('foo')
        self.assertEquals(stack.pop(), 'foo')
        stack.push('bar')
        self.assertEquals(stack.pop(), 'bar')

    def test_get_item(self):
        count = 100
        items = [i for i in range(count)]
        self.stack.extend(items)
        items.reverse()
        # Get single values
        for i in range(count):
            self.assertEquals(self.stack[i], items[i])
        # Get small ranges
        for i in range(count-1):
            self.assertEquals(self.stack[i:i+2], items[i:i+2])
        # Now get the whole range
        self.assertEquals(self.stack[0:-1], items[0:-1])
        self.stack.clear()

    def test_extend(self):
        '''Test extending a queue, including with a generator'''
        count = 100
        self.stack.extend(i for i in range(count))
        self.assertEquals(self.stack.elements(), [count - i - 1 for i in range(count)])
        
        # Also, make sure it's still a stack. It should be in reverse order
        last = self.stack.pop()
        while last != None:
            now = self.stack.pop()
            self.assertTrue(last > now)
            last = now
        self.stack.clear()

    def test_dump_load(self):
        # Get a temporary file to dump a queue to that file
        count = 100
        self.stack.extend(range(count))
        self.assertEquals(self.stack.elements(), [count - i - 1 for i in range(count)])
        with os.tmpfile() as f:
            self.stack.dump(f)
            # Now, assert that it is empty
            self.assertEquals(len(self.stack), 0)
            # Now, try to load it back in
            f.seek(0)
            self.stack.load(f)
            self.assertEquals(len(self.stack), count)
            self.assertEquals(self.stack.elements(), [count - i - 1 for i in range(count)])
            # Now clean up after myself
            f.truncate()
            self.stack.clear()

class PriorityQueue(unittest.TestCase):
    def setUp(self):
        r.delete('qrpriorityqueue')
        self.q = qr.PriorityQueue(key='qrpriorityqueue')

    def test_roundtrip(self):
        self.q.push('foo', 1)
        self.assertEquals(len(self.q), 1)
        self.assertEquals(self.q.pop(), 'foo')
        self.assertEquals(len(self.q), 0)

    def test_order(self):
        self.q.push('foo', 1)
        self.q.push('bar', 0)
        self.assertEquals(self.q.pop(), 'bar')
        self.assertEquals(self.q.pop(), 'foo')

    def test_get_item(self):
        count = 100
        items = [i for i in range(count)]
        self.q.extend(zip(items, items))
        # Get single values
        for i in range(count):
            self.assertEquals(self.q[i], items[i])
        # Get small ranges
        for i in range(count-1):
            self.assertEquals(self.q[i:i+2], items[i:i+2])
        # Now get the whole range
        self.assertEquals(self.q[0:-1], items[0:-1])
        self.q.clear()

    def test_extend(self):
        '''Test extending a queue, including with a generator'''
        count = 100
        items = [i for i in range(count)]
        self.q.extend(zip(items, items))
        self.assertEquals(self.q.elements(), items)
        self.q.clear()

    def test_pop(self):
        '''Test whether or not we can get real values with pop'''
        count = 100
        items = [i for i in range(count)]
        self.q.extend(zip(items, items))
        next = self.q.pop()
        while next:
            self.assertTrue(isinstance(next, int))
            next = self.q.pop()
        # Now we'll pop with getting the scores as well
        items = [i for i in range(count)]
        self.q.extend(zip(items, items))
        value, score = self.q.pop(withscores=True)
        while value:
            self.assertTrue(isinstance(value, int))
            self.assertTrue(isinstance(score, float))
            value, score = self.q.pop(withscores=True)
        
    def test_push(self):
        '''Test whether we can push well'''
        count = 100
        for i in range(count):
            self.q.push(i, count - i)
        value, score = self.q.pop(withscores=True)
        while value:
            self.assertEqual(value + score, count)
            value, score = self.q.pop(withscores=True)
        
    def test_uniqueness(self):
        count = 100
        # Push the same value on with different scores
        for i in range(count):
            self.q.push(1, i)
        self.assertEquals(len(self.q), 1)
        self.q.clear()
    
    def test_dump_load(self):
        # Get a temporary file to dump a queue to that file
        count = 100
        items = [i for i in range(count)]
        self.q.extend(zip(items, items))
        self.assertEquals(self.q.elements(), items)
        with os.tmpfile() as f:
            self.q.dump(f)
            # Now, assert that it is empty
            self.assertEquals(len(self.q), 0)
            # Now, try to load it back in
            f.seek(0)
            self.q.load(f)
            self.assertEquals(len(self.q), count)
            self.assertEquals(self.q.elements(), items)
            # Now clean up after myself
            f.truncate()
            self.q.clear()

if __name__ == '__main__':
    unittest.main()
