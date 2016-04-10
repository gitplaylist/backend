from flask import Flask
from flask_restful import Api, Resource
from flask.ext.assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
api = Api()
assets = Environment()
scss = Bundle('scss/style.scss',filters='scss', output='css/app.css')
assets.register('scss', scss)


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
    from models.dummy import Dummy

    with app.app_context():
        db.create_all()

    return app
