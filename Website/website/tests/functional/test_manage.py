from website.tests import *

class TestManageController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='manage', action='index'))
        # Test response...
