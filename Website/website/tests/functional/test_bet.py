from website.tests import *

class TestBetController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='bet', action='index'))
        # Test response...
