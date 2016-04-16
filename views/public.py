from flask import Blueprint, render_template

bp = Blueprint('public', __name__)

@bp.route('/')
def index(path=None):
    return render_template('public/index.html')

@bp.route('/login')
def login(path=None):
    return render_template('public/login.html')

@bp.route('/sign_up')
def signup(path=None):
    return render_template('public/sign_up.html')
