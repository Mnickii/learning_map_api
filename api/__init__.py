from flask import Flask
from flask_migrate import Migrate

from .models import db
from .config import app_configuration


# initialize Flask
def create_flask_app(env='production'):
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(app_configuration[env])

    # if env == 'development':
    #     app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
