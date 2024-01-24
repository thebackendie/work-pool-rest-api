from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, date
from enum import Enum
from flask_bcrypt import generate_password_hash, check_password_hash
from application.utils import db


class AccountType(Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super-admin"


class Users(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    login_attempts = db.Column(db.Integer(), nullable=True, default=0)
    is_active = db.Column(db.Boolean(), default=True)
    account_type = db.Column(db.Enum(AccountType), default=AccountType.USER)
    date_created = db.Column(db.Date(), default=date.today())
    date_updated = db.Column(db.Date(), onupdate=date.today())

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.first_name} {self.last_name}>"

    # Custom Methods
    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Query Methods
    @classmethod
    def user_exists_by_email(cls, email):
        return True if cls.query.filter_by(email=email).first() else False

    @classmethod
    def user_exists_by_user_id(cls, user_id):
        return True if cls.query.filter_by(user_id=user_id).first() else False

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_user_data_by_email(cls, email):
        user = cls.find_by_email(email)
        return None if user is None else user.to_dict(only=('first_name', 'last_name', 'email',
                                                            'is_active', 'account_type', 'date_created',
                                                            'date_updated'))

    @classmethod
    def get_user_data_by_id(cls, user_id):
        user = cls.find_by_user_id(user_id)
        return None if user is None else user.to_dict(only=('first_name', 'last_name', 'email',
                                                            'is_active', 'account_type', 'date_created',
                                                            'date_updated'))

    @classmethod
    def get_all_users_data(cls):
        users = cls.query.all()
        return [user.to_dict(only=('first_name', 'last_name', 'email',
                                   'login_attempts', 'is_active', 'account_type'))
                for user in users]

    @classmethod
    def count_all_users(cls):
        return cls.query.all().count()

    @classmethod
    def count_all_active_users(cls):
        return cls.query.filter(cls.is_active is True).count()

    @classmethod
    def count_all_inactive_users(cls):
        return cls.query.filter(cls.is_active is False).count()

    # Database Transaction Methods
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
