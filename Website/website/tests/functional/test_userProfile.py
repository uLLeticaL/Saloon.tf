from website.tests import *

class TestUserprofileController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='userProfile', action='index'))
        # Test response...
