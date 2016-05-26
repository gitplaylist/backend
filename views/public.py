from __future__ import absolute_import
from flask import Blueprint, render_template, request, redirect, url_for
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user

from app import db
from models.account import User

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('app.html')
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
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('public.index'))
        return render_template(self.template)

bp.add_url_rule('/sign_up', view_func=Signup.as_view('sign_up'))


class Login(MethodView):
    template = 'public/login.html'

    def get(self):
        return render_template(self.template)

    def post(self):
        user = User.query.filter(User.email == request.form.get('email')).first()
        if user.verify_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('public.index'))
        return render_template(self.template)

bp.add_url_rule('/login', view_func=Login.as_view('login'))

class Logout(MethodView):

    def get(self):
        logout_user()
        return redirect(url_for('public.index'))

bp.add_url_rule('/logout', view_func=Logout.as_view('logout'))
