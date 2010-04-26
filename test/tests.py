import unittest
import qr
import redis

r = redis.Redis()

class Queue(unittest.TestCase):
    def setUp(self):
	r.delete('qrtestqueue')
        self.q = qr.Queue(key='qrtestqueue')
        self.assertEquals(len(self.q.elements()), 0)

    def test_roundtrip(self):
        q = self.q
        q.push('foo')
        self.assertEquals(len(q.elements()), 1)
        self.assertEquals(q.pop(), 'foo')
        self.assertEquals(len(q.elements()), 0)

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

class CappedCollection(unittest.TestCase):
    def setUp(self):
	r.delete('qrtestcc')
       	self.aq = qr.CappedCollection(key='qrtestcc', size=3)
        self.assertEquals(len(self.aq.elements()), 0)

    def test_roundtrip(self):
        aq = self.aq
        aq.push('foo')
        self.assertEquals(len(aq.elements()), 1)
        self.assertEquals(aq.pop(), 'foo')
        self.assertEquals(len(aq.elements()), 0)

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
        self.assertEquals(len(aq.elements()), 3)
        aq.push('d')
        aq.push('e')
        self.assertEquals(len(aq.elements()), 3)
        self.assertEquals(aq.pop(), 'c')
        self.assertEquals(aq.pop(), 'd')
        self.assertEquals(aq.pop(), 'e')
        self.assertEquals(len(aq.elements()), 0)

class Stack(unittest.TestCase):
    def setUp(self):
	r.delete('qrteststack')
        self.stack = qr.Stack(key='qrteststack')

    def test_roundtrip(self):
        stack = self.stack
        stack.push('foo')
        self.assertEquals(len(stack.elements()), 1)
        self.assertEquals(stack.pop(), 'foo')
        self.assertEquals(len(stack.elements()), 0)

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

if __name__ == '__main__':
    unittest.main()

	

