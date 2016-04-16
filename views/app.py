from flask import Blueprint, render_template

bp = Blueprint('app', __name__)

# @bp.route('/')
# @bp.route('/<path:path>')
def serve_app(path=None):
    return render_template('app.html')
