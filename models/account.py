from passlib.apps import custom_app_context as pwd_context

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
