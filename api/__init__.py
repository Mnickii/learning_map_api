import os

from flask import Flask
from flask_migrate import Migrate, MigrateCommand

from api.models import db
from api.contributions.views import contributions_blueprint
from config import app_configuration


def create_app(configuration_name):
    # initialize Flask
    app = Flask(__name__, instance_relative_config=True, static_folder=None)

    # switch environment configuration
    if not configuration_name:
        configuration_name = 'production'

    app.config.from_object(app_configuration[configuration_name])

    if configuration_name == 'development':
        app.config.from_pyfile('config.py')

    # initialize SQLAlchemy
    from api import models
    db.init_app(app)

    # initialize flask migrate
    migrate = Migrate(app, db)

    app.register_blueprint(contributions_blueprint, url_prefix='/api/v1')

    return app
