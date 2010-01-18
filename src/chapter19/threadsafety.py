import threading
import time
import unittest

class ThreadSafetyTestCase(unittest.TestCase):

    def assertContended(self, f, first, second, num_threads=20, timeout=2.):
        threads = []
        for i in xrange(num_threads):
            t = threading.Thread(target=f)
            t.start()
            threads.append(t)
        for t in threads:
            t.join(timeout)
            timeout = 0.
        for t in threads:
            self.assertFalse(t.isAlive())
        self.assertEqual(first, second)


# which we can then use like so

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
