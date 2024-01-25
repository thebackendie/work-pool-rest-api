import re
from http import HTTPStatus
from flask import make_response, jsonify
from flask_jwt_extended import create_refresh_token, create_access_token, decode_token
from flask_restx import Resource, Namespace, fields
from application.models.v1.users import Users, AccountType
from application.utils.apiError import ApiError
from application.utils.utils_func import add_token_to_database

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
        first_name = auth_namespace.payload.get("first_name")
        last_name = auth_namespace.payload.get("last_name")
        email = auth_namespace.payload.get("email")
        password = auth_namespace.payload.get("password").encode('utf-8')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ApiError('Invalid email format.', HTTPStatus.BAD_REQUEST)
        user = Users.user_exists_by_email(email)
        if user:
            raise ApiError("A user with this email already exists!", HTTPStatus.BAD_REQUEST)
        else:
            user = Users()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password_hash(password)
            user.save_to_db()
            data = user.get_user_data_by_email(email)
        response = {
            "is_success": True,
            "msg": "Account created successfully",
            "data": data
        }
        return make_response(jsonify(response), HTTPStatus.CREATED)


@auth_namespace.route("/users/login")
class LoginUser(Resource):
    @auth_namespace.expect(login_user_model, validate=True)
    def post(self):
        email = auth_namespace.payload.get("email")
        password = auth_namespace.payload.get("password").encode('utf-8')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ApiError('Invalid email format.', HTTPStatus.BAD_REQUEST)
        user = Users.find_by_email(email)
        if user is None:
            raise ApiError("Invalid email or password", HTTPStatus.BAD_REQUEST)
        elif user:
            if user.is_active is False:
                raise ApiError("Account has been blocked for violating terms and conditions. Kindly contact "
                               "administrators. Thank you", HTTPStatus.FORBIDDEN)
            if user.login_attempts >= 5:
                raise ApiError("Account has blocked due to maximum number of failed login attempts",
                               HTTPStatus.FORBIDDEN)
            if user and user.check_password(password):
                account_type = None
                match user.account_type:
                    case AccountType.USER:
                        account_type = "user"
                    case AccountType.ADMIN:
                        account_type = "admin"
                    case AccountType.SUPER_ADMIN:
                        account_type = "super-admin"
                identity = {"id": user.id, "account_type": account_type}
                access_token = create_access_token(identity=identity)
                refresh_token_sibling = decode_token(access_token)
                refresh_token_sibling_jti = refresh_token_sibling['jti']
                refresh_token = create_refresh_token(identity=identity)
                access_token_sibling = decode_token(refresh_token)
                access_token_sibling_jti = access_token_sibling['jti']
                add_token_to_database(token=access_token, sibling_jti=access_token_sibling_jti,
                                      owners_id=user.id, owners_account_type="User")
                add_token_to_database(token=refresh_token, sibling_jti=refresh_token_sibling_jti,
                                      owners_id=user.id, owners_account_type="User")
                user.login_attempts = 0
                user.save_to_db()
                user = user.get_user_data_by_email(email)

                response = {
                    "is_success": True,
                    "msg": "Login Successful",
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user
                    }
                }
                return make_response(jsonify(response), HTTPStatus.OK)
            else:
                user.login_attempts += 1
                user.save_to_db()
                raise ApiError("Invalid email or password", HTTPStatus.BAD_REQUEST)


@auth_namespace.route("/logout")
class Logout(Resource):
    def post(self):
        response = {
            "is_success": True,
            "message": "Logged out successfully"
        }
        return make_response(jsonify(response), HTTPStatus.OK)