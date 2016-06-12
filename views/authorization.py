from __future__ import absolute_import
from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_user

from models.account import User

bp = Blueprint('authorization', __name__)


class Authorize(MethodView):

    def post(self):
        user = User.query.filter(User.email == request.form.get('email')).first()
        if user.verify_password(request.form.get('password')):
            login_user(user)
            return user.id
        return {'message': 'Invaild authorization information given'}, 400

bp.add_url_rule('/users/authorize', view_func=Authorize.as_view('authorize'))
