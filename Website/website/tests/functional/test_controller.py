from website.tests import *

class TestControllerController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='controller', action='index'))
        # Test response...
