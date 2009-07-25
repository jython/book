from rostertool.tests import *

class TestRosterController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='roster', action='index'))
        # Test response...
