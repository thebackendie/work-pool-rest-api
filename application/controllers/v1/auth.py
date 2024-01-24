import re
from http import HTTPStatus
from flask import make_response, jsonify
from flask_restx import Resource, Namespace, fields

auth_namespace = Namespace("Auth", description="A namespace for authentication")

# Controllers for Users
register_user_model = auth_namespace.model('Register User', {
    'first_name': fields.String(required=True, help="First name is required", min_length=2),
    'last_name': fields.String(required=True, help="Last name is required", min_length=2),
    'email': fields.String(required=True, help="Email is required", min_length=5),
    'password': fields.String(required=True, help="Password is required", min_length=8)
})

login_user_model = auth_namespace.model('Login User', {
    'email': fields.String(required=True, help="Email is required", min_length=5),
    'password': fields.String(required=True, help="Password is required", min_length=2)
})


@auth_namespace.route("/users/join")
class RegisterUser(Resource):
    @auth_namespace.expect(register_user_model, validate=True)
    def post(self):
        response = {
            "is_success": True,
            "msg": "Account created successfully",
        }
        return make_response(jsonify(response), HTTPStatus.OK)


@auth_namespace.route("/users/login")
class LoginUser(Resource):
    @auth_namespace.expect(login_user_model, validate=True)
    def post(self):
        response = {
            "is_success": True,
            "msg": "User logged in successfully",
        }
        return make_response(jsonify(response), HTTPStatus.OK)


@auth_namespace.route("/logout")
class Logout(Resource):
    def post(self):
        response = {
            "is_success": True,
            "message": "Logged out successfully"
        }
        return make_response(jsonify(response), HTTPStatus.OK)