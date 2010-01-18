from threading import Thread
import time

def make_imports():
    import unicodedata

background_import = Thread(target=make_imports)
background_import.start()

print "Do something else while we wait for the import"
for i in xrange(10):
    print i
    time.sleep(0.1)
print "Now join..."
background_import.join()

print "And actually use unicodedata"
import unicodedata

