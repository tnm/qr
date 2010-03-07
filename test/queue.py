import unittest
import qr

class Queue(unittest.TestCase):
    """Test a bounded queue, without automatic popping of elements"""
    def setUp(self):
        self.q = qr.Queue(key='queue', size=3)
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
        self.assertEquals(q.pop(), 'a')
        self.assertEquals(q.pop(), 'b')
        self.assertEquals(q.pop(), 'c')
        self.assertEquals(len(q.elements()), 0)

class AutoQueue(unittest.TestCase):
    """Test a bounded queue, with automatic popping of elements"""
    def setUp(self):
        self.aq = qr.Queue(key='autoqueue', size=3, auto=True)
        self.assertEquals(len(self.q.elements()), 0)

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
	

