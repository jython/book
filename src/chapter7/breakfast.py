class Spam(object):

    def order(self, number):
        print "spam " * number

def order_eggs():
    print " and eggs!"

s = Spam()
s.order(3)
order_eggs()

