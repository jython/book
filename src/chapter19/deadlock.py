from __future__ import with_statement
from threading import Thread, Lock
from java.lang.management import ManagementFactory
import time, threading

def cause_deadlock():
    counter = [0]
    lock_one = Lock()
    lock_two = Lock()
    threads = [
        Thread(
            name="thread #1", target=acquire_locks,
            args=(counter, lock_one, lock_two)), 
        Thread(
            name="thread #2 (reversed)", target=acquire_locks,
            args=(counter, lock_two, lock_one))]
    for thread in threads:
        thread.setDaemon(True) # make shutdown possible after deadlock
        thread.start()

    thread_mxbean = ManagementFactory.getThreadMXBean()
    while True:
        time.sleep(1)
        print "monitoring thread", counter[0]
        thread_ids = thread_mxbean.findDeadlockedThreads()
        if thread_ids:
            print "monitoring thread: deadlock detected, shutting down", list(thread_ids)
            break

def acquire_locks(counter, lock1, lock2):
    # Should eventually deadlock if locks are acquired in different order
    name = threading.currentThread().getName()
    while True:
        with lock1:
            with lock2:
                counter[0] += 1
                print name, counter[0]


if __name__ == '__main__':
    cause_deadlock()
