from sqlalchemy_serializer import SerializerMixin
from datetime import date
from application.utils import db


class TokenBlacklist(db.Model, SerializerMixin):
    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(200), nullable=False)
    sibling_jti = db.Column(db.String(200), nullable=False)
    token_type = db.Column(db.String(10))
    owners_id = db.Column(db.Integer, nullable=False)
    owners_account_type = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    revoked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.Date(), default=date.today())
    expires = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Token {self.jti}> "

    def save(self):
        db.session.add(self)
        db.session.commit()
