from flask import Blueprint, render_template, request
from flask.views import MethodView
from flask_login import login_user

from models.account import User

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    return render_template('public/index.html')

class Signup(MethodView):
    template = 'public/sign_up.html'

    def get(self):
        return render_template(self.template)

    def post(self):
        user = User(
            request.form.get('email'),
            request.form.get('password'),
        )
        # db.session.add(user)
        # db.session.commit()
        login_user(user)
        return render_template(self.template)

bp.add_url_rule('/sign_up', view_func=Signup.as_view('sign_up'))


class Login(MethodView):
    template = 'public/login.html'

    def get(self):
        return render_template(self.template)

    def post(self):
        user = User.query.get(email=request.form.get('email'))
        if user.verify_password(request.form.get('password')):
            login_user(user)
        return render_template(self.template)

bp.add_url_rule('/login', view_func=Login.as_view('login'))
