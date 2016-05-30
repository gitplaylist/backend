from passlib.apps import custom_app_context as pwd_context

from flask_login import UserMixin
from flask_validator import ValidateEmail

from app import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % (self.email)

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(User.email)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
