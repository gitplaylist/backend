import os

from flask import Flask
from flask_restful import Api, Resource
from flask.ext.assets import Environment, Bundle
from webassets.filter import register_filter
from webassets_browserify import Browserify
from flask_sqlalchemy import SQLAlchemy
from config import Config


register_filter(Browserify)

db = SQLAlchemy()
api = Api()
assets = Environment()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
assets.from_yaml(os.path.join(APP_ROOT, 'static/assets.yml'))

def create_app():
    app = Flask(__name__)
    app.config.update(Config.__dict__)

    # Set up extensions
    db.init_app(app)
    app.db = db

    api.init_app(app)
    assets.init_app(app)

    # Install views
    from views.index import bp as index_bp
    app.register_blueprint(index_bp)

    # Install models
    from models.account import User

    with app.app_context():
        db.create_all()

    return app
