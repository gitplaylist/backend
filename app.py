from flask import Flask
from flask_restful import Api, Resource
from flask.ext.assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
assets = Environment(app)
scss = Bundle('scss/style.scss',filters='scss', output='css/app.css')
assets.register('scss', scss)
app.config.update(Config.__dict__)
