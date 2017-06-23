from learning_map_api.api import create_flask_app
from learning_map_api.api.test.base import BaseTestCase
# import unittest


class TestMain(BaseTestCase):
    def test_app_get(self):
        self.app = self.app.test_client()
        response = self.app.get('/')
        # this should be changed to assert200, it's a bug
        self.assert404(response)
