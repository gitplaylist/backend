from flask import Blueprint, render_template


bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    return render_template('public/index.html')

@bp.route('/login')
def login():
    return render_template('public/login.html')

@bp.route('/sign_up')
def signup():
    return render_template('public/sign_up.html')
