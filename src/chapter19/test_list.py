from threadsafety import ThreadSafetyTestCase
import threading
import time
import unittest

class ListThreadSafety(ThreadSafetyTestCase):

    def test_append_remove(self):
        lst = []
        def tester():
            # preserve invariant by adding, then removing a unique
            # value (in this case, a reference to the worker thread
            # executing this function)
            ct = threading.currentThread()
            for i in range(1000):
                lst.append(ct)
                time.sleep(0.0001)
                lst.remove(ct)
        self.assertContended(tester, lst, [])



if __name__ == '__main__':
    unittest.main()
