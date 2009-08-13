import unittest

class TestLists(unittest.TestCase):
    def setUp(self):
        self.list = ['foo', 'bar', 'baz']

    def testLen(self):
        self.assertEqual(3, len(self.list))

    def testContains(self):
        self.assert_('foo' in self.list)
        self.assert_('bar' in self.list)
        self.assert_('baz' in self.list)

    def testSort(self):        
        self.assertNotEqual(['bar', 'baz', 'foo'], self.list)
        self.list.sort()
        self.assertEqual(['bar', 'baz', 'foo'], self.list)
            
if __name__ == '__main__':
    unittest.main()
