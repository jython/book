import threading
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


