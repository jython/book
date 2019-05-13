from __future__ import print_function
print("in greet/hello.py")
import people

class Greeter(object):
    def hello_all(self):
        for name in people.names:
            print("hello %s" % name)
