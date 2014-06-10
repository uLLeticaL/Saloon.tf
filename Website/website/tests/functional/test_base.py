from website.tests import *

class TestBaseController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='base', action='index'))
        # Test response...
