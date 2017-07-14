from learning_map_api.api.test.base import BaseTestCase


class TestMain(BaseTestCase):
    def test_app_get(self):
        response = self.client.get('/')
        self.assert200(response)
