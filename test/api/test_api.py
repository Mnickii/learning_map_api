from learning_map_api.main import create_flask_app
from learning_map_api.test.base import BaseTestCase


class TestApiInitialization(BaseTestCase):

    def test_testing_config(self):
        app = create_flask_app('testing')
        self.assertTrue(app.config.get('TESTING'))

    def test_development_config(self):
        app = create_flask_app('development')

        # quite a lame assert I agree
        self.assertFalse(app.config.get('TESTING'))

    def test_production_config(self):
        app = create_flask_app('production')

        # quite a lame assert I agree
        self.assertFalse(app.config.get('TESTING'))
