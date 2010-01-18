from downloader import Downloader
from shutdown import shutdown_and_await_termination
from java.util.concurrent import Executors, ExecutorCompletionService
import os
import hashlib

MAX_CONCURRENT = 3
SITES = [
    "http://www.cnn.com/",
    "http://www.nytimes.com/",
    "http://www.washingtonpost.com/",
    "http://www.dailycamera.com/",
    "http://www.timescall.com/",
    # generate a random web site name that is very, very unlikely to exist
    "http://" + hashlib.md5(
        "unlikely-web-site-" + os.urandom(4)).hexdigest() + ".com",
    ]

pool = Executors.newFixedThreadPool(MAX_CONCURRENT)
ecs = ExecutorCompletionService(pool)

# this function could spider the links from these roots;
# for now just schedule these roots directly
def scheduler(roots):
    for site in roots:
        yield site

# submit tasks indefinitely
for site in scheduler(SITES):
    ecs.submit(Downloader(site))

# work with results as soon as they become available
submitted = len(SITES)
while submitted > 0:
    result = ecs.take().get()
    # here we just do something unimaginative with the result;
    # consider parsing it with tools like beautiful soup
    print result
    submitted -= 1

print "shutting pool down..."
shutdown_and_await_termination(pool, 5)
print "done"
