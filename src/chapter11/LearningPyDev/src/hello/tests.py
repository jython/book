import unittest
import hello

class UIMock(object):
    def __init__(self):
        self.msgs = []
    def __call__(self, msg):
        self.msgs.append(msg)    

class TestUIs(unittest.TestCase):
    def setUp(self):        
        global hello
        hello = reload(hello)
        self.foo = UIMock()
        self.bar = UIMock()
        hello.register_ui('foo')(self.foo)    
        hello.register_ui('bar')(self.bar)
        hello.message('foo', "message using the foo UI")
        hello.message('foo', "another message using foo")
        hello.message('bar', "message using the bar UI")
    
    def testBarMessages(self):
        self.assertEqual(["message using the bar UI"], self.bar.msgs) 
    
    def testFooMessages(self):
        self.assertEqual(["message using the foo UI", 
                          "another message using foo"],
                          self.foo.msgs)    
    def testNonExistentUI(self):
        self.assertRaises(hello.UINotSupportedExeption, 
                          hello.message, 'non-existent-ui', 'msg')

    def testListUIs(self):
        uis = hello.list_uis()
        self.assertEqual(2, len(uis))
        self.assert_('foo' in uis)
        self.assert_('bar' in uis)

