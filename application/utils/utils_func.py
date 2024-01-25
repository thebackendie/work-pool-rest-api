import math
import random
from datetime import datetime
from http import HTTPStatus

from flask_jwt_extended import decode_token
from sqlalchemy.exc import NoResultFound

from .apiError import ApiError
from application.models.v1.token_blacklist import TokenBlacklist


def generate_password():
    random_str = ""
    digits = [i for i in range(0, 10)]

    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
        # # displaying the random string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    generated_password = ""
    length = len(string)
    for i in range(8):
        generated_password += string[math.floor(random.random() * length)]
    return generated_password


def add_token_to_database(token, sibling_jti, owners_id, owners_account_type):
    token_to_db = TokenBlacklist()
    decoded_token = decode_token(token)
    token_to_db.jti = decoded_token['jti']
    token_to_db.sibling_jti = sibling_jti
    token_to_db.token_type = decoded_token['type']
    token_to_db.owners_id = owners_id
    token_to_db.owners_account_type = owners_account_type
    token_to_db.expires = datetime.fromtimestamp(decoded_token["exp"])
    token_to_db.save()


def revoke_token(jti, owners_id):
    try:
        token = TokenBlacklist.query.filter_by(jti=jti, owners_id=owners_id, is_active=True).one()
        token.is_active = False
        token.revoked_at = datetime.utcnow()
        token.save()
        sibling_token = TokenBlacklist.query.filter_by(jti=token.sibling_jti, is_active=True).one()
        sibling_token.is_active = False
        sibling_token.revoked_at = datetime.utcnow()
        sibling_token.save()
    except NoResultFound:
        raise ApiError("Invalid token",  HTTPStatus.BAD_REQUEST)


def revoke_access_token(sibling_jti, owners_id):
    try:
        token = TokenBlacklist.query.filter_by(sibling_jti=sibling_jti, owners_id=owners_id, is_active=True).one()
        token.is_active = False
        token.revoked_at = datetime.utcnow()
        token.save()
    except NoResultFound:
        raise ApiError("Invalid token",  HTTPStatus.BAD_REQUEST)
