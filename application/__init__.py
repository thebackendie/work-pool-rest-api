from http import HTTPStatus
import sqlalchemy
from flask import Flask, make_response, jsonify
from flask_restx import Api
from .config.v1.config import config_dict


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app)

    return app
