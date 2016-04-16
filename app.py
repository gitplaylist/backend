from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
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

    api.init_app(app)
    assets.init_app(app)
    login_manager.init_app(app)

    # Install views
    from views.app import bp as app_bp
    from views.public import bp as public_bp
    app.register_blueprint(app_bp)
    app.register_blueprint(public_bp)

    # Install models
    from models.account import User

    with app.app_context():
        db.create_all()

    return app
