from __future__ import absolute_import
from flask import request
from flask_login import login_user, logout_user
from flask_restful import Resource

from app import api
from models.account import User


class Authorize(Resource):

    def post(self):
        user = User.query.filter(User.email == request.form.get('email')).first()
        if user and user.verify_password(request.form.get('password')):
            login_user(user)
            return user.id
        return {'message': 'Invaild authorization information given'}, 400

api.add_resource(Authorize, '/users/authorize')

class Logout(Resource):

    def post(self):
        logout_user()
        return ''

api.add_resource(Logout, '/users/logout')
