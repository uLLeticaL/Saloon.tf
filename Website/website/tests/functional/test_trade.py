from website.tests import *

class TestTradeController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='trade', action='index'))
        # Test response...
