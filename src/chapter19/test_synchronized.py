from synchronize import make_synchronized
from threadsafety import ThreadSafetyTestCase
import time
import unittest

@make_synchronized
def increment_counter(counter):
    counter[0] += 1
    # sleeping helps ensures that all threads run in our test
    time.sleep(0.0001)

class SynchronizedTestCase(ThreadSafetyTestCase):
    
    def test_counter(self):
        def loop100(counter):
            for i in xrange(100):
                increment_counter(counter)

        counter = [0]
        self.assertContended(loop100, args=(counter,), num_threads=20)
        self.assertEqual(counter[0], 2000) # 20 threads * 100 loops/thread

if __name__ == '__main__':
    unittest.main()
