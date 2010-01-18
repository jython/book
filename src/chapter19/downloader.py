import threading
import time
import urllib2
from java.util.concurrent import Callable

class Downloader(Callable):
    def __init__(self, url):
        self.url = url
        self.started = None
        self.completed = None
        self.result = None
        self.thread_used = None
        self.exception = None

    def __str__(self):
        if self.exception:
             return "[%s] %s download error %s in %.2fs" % \
                (self.thread_used, self.url, self.exception, self.completed - self.started, ) #, self.result)
        elif self.completed:
            return "[%s] %s downloaded %dK in %.2fs" % \
                (self.thread_used, self.url, len(self.result)/1024, self.completed - self.started, ) #, self.result)
        elif self.started:
            return "[%s] %s started at %s" % \
                (self.thread_used, self.url, self.started)
        else:
            return "[%s] %s not yet scheduled" % \
                (self.thread_used, self.url)

    # needed to implement the Callable interface;
    # any exceptions will be wrapped as either ExecutionException
    # or InterruptedException
    def call(self):
        self.thread_used = threading.currentThread().getName()
        self.started = time.time()
        try:
            self.result = urllib2.urlopen(self.url).read()
        except Exception, ex:
            self.exception = ex
        self.completed = time.time()
        return self

