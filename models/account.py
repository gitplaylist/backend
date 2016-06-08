from collections import defaultdict

from app import db, login_manager
from flask_login import UserMixin
from flask_validator import ValidateEmail, ValidateError, ValidateLength
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.sql import func


class GithubAccessToken(db.Model):
    __tablename__ = 'github_accesstoken'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    token_type = db.Column(db.String(16))
    scope = db.Column(db.String(64))
    access_token = db.Column(db.String(40), unique=True)

    date_created = db.Column(
        db.DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(
        db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user_id, token_type, scope, access_token):
        self.user_id = user_id
        self.token_type = token_type
        self.scope = scope
        self.access_token = access_token

    def __repr__(self):
        return '<GithubAccessToken {} of {}>'.format(
            self.access_token,
            self.user
        )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    github_accesstoken = db.relationship(
        GithubAccessToken, uselist=False, back_populates="user")

    date_created = db.Column(
        db.DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(
        db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, email, password=None):
        self.email = email
        self.password_hash = self.hash_password(password) if password else None

    def __repr__(self):
        return '<User %r>' % (self.email)

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        if self.password_hash:
            return pwd_context.verify(password, self.password_hash)
        else:
            return False

    @classmethod
    def __declare_last__(cls):
        errors = defaultdict(list)

        # if ValidateEmail(User.email):
        #     errors['email'] = 'invalid email'
        # if ValidateLength(User.password_hash, min_length=8, max_length=128):
        #     errors['password'] = 'invalid password length'

        if errors:
            raise ValidateError(errors)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
