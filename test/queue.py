import unittest
import qr

class Queue(unittest.TestCase):
    def setUp(self):
        self.q = qr.Queue(key='queue', size=3)
        qr.redis.flushdb()
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

    def test_limit(self):
        q = self.q
        q.push('a')
        q.push('b')
        q.push('c')
        self.assertEquals(len(q.elements()), 3)
        q.push('d')
        q.push('e')
        self.assertEquals(len(q.elements()), 3)
        self.assertEquals(q.pop(), 'c')
        self.assertEquals(q.pop(), 'd')
        self.assertEquals(q.pop(), 'e')
        self.assertEquals(len(q.elements()), 0)

