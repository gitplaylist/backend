from flask import Blueprint, render_template
from app import api
from flask_restful import Resource

bp = Blueprint('index', __name__)

@bp.route('/')
def serve_app():
    return render_template('index.html')


class HelloWorld(Resource):
    """
     Hello world
    """

    def get(self):
        return {'hello': 'world'}
api.add_resource(HelloWorld, '/helloworld')
