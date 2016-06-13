from config import Config

from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from webassets.filter import register_filter
from webassets_browserify import Browserify

register_filter(Browserify)

db = SQLAlchemy()
api = Api()
assets = Environment()
login_manager = LoginManager()
oauth = OAuth()

github = oauth.remote_app(
    'Github OAuth',
    base_url="https://api.github.com/",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    consumer_key=Config.GITHUB_CLIENT_ID,
    consumer_secret=Config.GITHUB_CLIENT_SECRET,
)
def change_github_header(uri, headers, body):  # pragma: no cover
    auth = headers.get('Authorization')
    if auth:
        auth = auth.replace('Bearer', 'token')
        headers['Authorization'] = auth
    return uri, headers, body

github.pre_request = change_github_header

scss = Bundle('scss/*.scss', 'scss/components/*.scss', filters='scss', output='gen/app.css')
jsx = Bundle('jsx/*.jsx', filters='browserify', output='gen/app.js', depends='jsx/**/*.jsx')

assets.register('scss', scss)
assets.register('jsx', jsx)

def create_app():
    """ Initializing the app """
    app = Flask(__name__)
    app.config.update(Config.__dict__)

    # Set up extensions
    db.init_app(app)
    app.db = db
    Migrate(app, db)

    assets.init_app(app)
    login_manager.init_app(app)

    # Install views
    from views.app import bp as app_bp
    from views.oauth import bp as oauth_bp
    app.register_blueprint(app_bp)
    app.register_blueprint(oauth_bp)

    # Install API
    from views import account
    from views import authorization
    api.init_app(app)

    # Install models
    from models.account import User

    return app
