from flask import Flask, render_template
from flask_restful import Api, Resource
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
api = Api(app)
assets = Environment(app)
scss = Bundle('scss/style.scss',filters='scss', output='css/app.css')
assets.register('scss', scss)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@app.route('/')
def serve_app():
    return render_template('index.html')

api.add_resource(HelloWorld, '/helloworld')

if __name__ == '__main__':
    app.run(debug=True)
