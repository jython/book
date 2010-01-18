from __future__ import with_statement
from threading import Condition, Lock, Thread
from java.lang import Thread as JThread, InterruptedException
from monkeypatch import monkeypatch_method_if_not_set
import time, threading

@monkeypatch_method_if_not_set(Thread)
def __tojava__(self, java_type):
    return self._thread

def be_unfair():
    unfair_condition = Condition()
    threads = [
        Thread(
            name="thread #%d" % i,
            target=wait_until_interrupted,
            args=(unfair_condition,)) 
        for i in xrange(5)]
    for thread in threads:
        thread.start()
    time.sleep(5)

    # threads should not be doing anything now, can verify by looking at some shared state

    # instead of notifying, we will interrupt the threads
    for thread in threads:
        JThread.interrupt(thread)
        # or you can use this equivalent op
        # thread.__tojava__(JThread).interrupt()
    for thread in threads:
        thread.join()

def wait_until_interrupted(cv):
    name = threading.currentThread().getName()
    with cv:
        while not JThread.currentThread().isInterrupted():
            try:
                print "Waiting pointlessly %s" % name
                cv.wait()
            except InterruptedException, e:
                break
    print "Finished %s" % name


if __name__ == '__main__':
    be_unfair()
