import os

from flask import Flask
from flask_migrate import Migrate
from flask import jsonify
from flask_restful import Api

try:
    from config import app_configuration
    from api.views.contributions import ContributionsResource
    from api.views.paths import (
        PathResource
    )
except ModuleNotFoundError:
    from learning_map_api.config import app_configuration
    from learning_map_api.api.views.contributions import (
        ContributionsResource
    )
    from learning_map_api.api.views.paths import (
        PathResource
    )


def create_flask_app(environment):
    # initialize Flask
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(app_configuration[environment])

    # initialize SQLAlchemy
    try:
        from api import models
    except ModuleNotFoundError:
        from learning_map_api.api import models
    models.db.init_app(app)
    migrate = Migrate(app, models.db)

    # test route
    @app.route('/')
    def index():
        return "Welcome to the Learning map Api"

    # create endpoints
    api = Api(app)
    api.add_resource(ContributionsResource,
                     '/api/v1/contributions',
                     endpoint='contributions')
    api.add_resource(ContributionsResource,
                     '/api/v1/contributions/<string:id>')
    api.add_resource(PathResource, '/api/v1/paths', '/api/v1/paths/',
                     endpoint='paths')
    api.add_resource(PathResource, '/api/v1/paths/<string:id>',
                     '/api/v1/paths/<string:id>/', endpoint='single_path')


    # handle default 404 exceptions with a custom response
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify(dict(status=404, error='Not found', message='The '
                                'requested URL was not found on the server. If'
                                ' you entered the URL manually please check '
                                'your spelling and try again'))
        response.status_code = 404
        return response

    # handle default 500 exceptions with a custom response
    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify(dict(status=500, error='Internal server error',
                                message="It is not you. It is me. The server "
                                "encountered an internal error and was unable "
                                "to complete your request.  Either the server "
                                "is overloaded or there is an error in the "
                                "application"))
        response.status_code = 500
        return response

    return app


# enable the flask run command to work
app = create_flask_app(os.getenv("FLASK_CONFIG"))


if __name__ == "__main__":
    environment = os.getenv("FLASK_CONFIG")
    app = create_flask_app(environment)
    app.run()
