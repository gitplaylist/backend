from flask import Blueprint, Flask
from flask_assets import Bundle, Environment
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from webassets.filter import register_filter
from webassets_browserify import Browserify

from config import Config

register_filter(Browserify)

db = SQLAlchemy()
api = Api()
assets = Environment()
login_manager = LoginManager()
oauth = OAuth()

spotify = oauth.remote_app(
    'Spotify OAuth',
    consumer_key=Config.SPOTIFY_CLIENT_ID,
    consumer_secret=Config.SPOTIFY_CLIENT_SECRET,
    request_token_params={'scope': 'user-read-email'},
    base_url='https://api.spotify.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize',
)

github = oauth.remote_app(
    'Github OAuth',
    consumer_key=Config.GITHUB_CLIENT_ID,
    consumer_secret=Config.GITHUB_CLIENT_SECRET,
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)
def change_github_header(uri, headers, body):  # pragma: no cover
    auth = headers.get('Authorization')
    if auth:
        auth = auth.replace('Bearer', 'token')
        headers['Authorization'] = auth
    return uri, headers, body

github.pre_request = change_github_header

def create_app():
    """ Initializing the app """
    app = Flask(__name__)
    app.config.update(Config.__dict__)

    # Set up extensions
    db.init_app(app)
    app.db = db
    Migrate(app, db)
    CORS(app) # TODO: Don't allow all in production

    assets.init_app(app)
    login_manager.init_app(app)

    # Install views
    from views.oauth import bp as oauth_bp
    app.register_blueprint(oauth_bp)

    # Install API
    from views import account
    from views import authorization
    api.init_app(app)

    # Install models
    from models.account import User

    return app
