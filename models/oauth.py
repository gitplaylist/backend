from sqlalchemy.sql import func

from app import db


class GithubAccessToken(db.Model):
    """Represent a Github access token."""

    __tablename__ = 'github_accesstoken'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    token_type = db.Column(db.String(16))
    scope = db.Column(db.String(64))
    access_token = db.Column(db.String(64), unique=True)

    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

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

class SpotifyAccessToken(db.Model):
    """Represent a Spotify access token."""

    __tablename__ = 'spotify_accesstoken'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    access_token = db.Column(db.String(64), unique=True)
    token_type = db.Column(db.String(16))
    scope = db.Column(db.String(64))
    expires_in  = db.Column(db.Integer)
    refresh_token = db.Column(db.String(64), unique=True)

    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user_id, token_type, scope, access_token):
        self.user_id = user_id
        self.token_type = token_type
        self.scope = scope
        self.access_token = access_token

    def __repr__(self):
        return '<SpotifysToken {} of {}>'.format(
            self.access_token,
            self.user
        )
