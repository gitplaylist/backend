from app import db


class Dummy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
