from flask_testing import TestCase
from learning_map_api.api import create_flask_app
from learning_map_api.api.models import db


class BaseTestCase(TestCase):

    def create_app(self):
        self.app = create_flask_app("testing")
        self.app.config['LIVESERVER_TIMEOUT'] = 10
        self.app_context = self.app.app_context()
        self.app_context.push()
        return self.app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
