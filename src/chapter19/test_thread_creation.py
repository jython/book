from threading import Thread
import urllib2

downloaded_page = None # global

def download(url):
    """Download ``url`` as a single string"""
    global downloaded_page

    downloaded_page = urllib2.urlopen(url).read()
    print "Downloaded", downloaded_page[:200]


def main_work():
    # do some busy work in parallel
    print "Started main task"
    x = 0
    for i in xrange(100000000):
        x += 1
    print "Completed main task"

if __name__ == '__main__':
    # perform the download in the background
    Thread(target=lambda: download("http://www.jython.org")).start()
    main_work()


