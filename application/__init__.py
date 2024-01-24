from http import HTTPStatus
import sqlalchemy
from flask import Flask, make_response, jsonify
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from .config.v1.config import config_dict
from .controllers.v1.auth import auth_namespace
from .utils import db


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt = Bcrypt(app)

    # Routes
    api.add_namespace(auth_namespace, path="/api/v1/auth")

    return app
