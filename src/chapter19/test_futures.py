from downloader import Downloader
from shutdown import shutdown_and_await_termination
from java.util.concurrent import Executors, TimeUnit

MAX_CONCURRENT = 3
SITES = [
    "http://www.cnn.com/",
    "http://www.nytimes.com/",
    "http://www.washingtonpost.com/",
    "http://www.dailycamera.com/",
    "http://www.timescall.com/",
    ]

pool = Executors.newFixedThreadPool(MAX_CONCURRENT)
downloaders = [Downloader(url) for url in SITES]
futures = pool.invokeAll(downloaders)

for future in futures:
    print future.get(5, TimeUnit.SECONDS)

shutdown_and_await_termination(pool, 5)





