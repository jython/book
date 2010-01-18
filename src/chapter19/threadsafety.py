import threading
import unittest

class ThreadSafetyTestCase(unittest.TestCase):

    def assertContended(self, f, num_threads=20, timeout=2., args=()):
        threads = []
        for i in xrange(num_threads):
            t = threading.Thread(target=f, args=args)
            t.start()
            threads.append(t)
        for t in threads:
            t.join(timeout)
            timeout = 0.
        for t in threads:
            self.assertFalse(t.isAlive())
