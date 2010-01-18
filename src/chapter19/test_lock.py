from __future__ import with_statement
from threading import Lock
from threadsafety import ThreadSafetyTestCase
import time
import unittest

class LockTestCase(ThreadSafetyTestCase):
    
    def test_with_lock(self):
        counter = [0]
        lock = Lock()
        def loop100(counter):
            for i in xrange(100):
                with lock:
                    counter[0] += 1
                # sleeping helps ensures that all threads run in our test
                time.sleep(0.0001)

        self.assertContended(loop100, args=(counter,), num_threads=20)
        self.assertEqual(counter[0], 2000) # 20 threads * 100 loops/thread

    def test_try_finally_lock(self):
        counter = [0]
        lock = Lock()
        def loop100(counter):
            for i in xrange(100):
                lock.acquire()
                try:
                    counter[0] += 1
                finally:
                    lock.release()
                time.sleep(0.0001)

        self.assertContended(loop100, args=(counter,), num_threads=20)
        self.assertEqual(counter[0], 2000)

    def test_unlocked_contention(self):
        # increase threads and loop iterations to make it very
        # unlikely the unlocked version will inadvertently pass this
        # test (but it still might)
        counter = [0]
        lock = Lock()
        def loop1000(counter):
            for i in xrange(1000):
                counter[0] += 1
                time.sleep(0.0001)

        self.assertContended(loop1000, args=(counter,), num_threads=200)
        self.assertNotEqual(counter[0], 200000)

if __name__ == '__main__':
    unittest.main()
