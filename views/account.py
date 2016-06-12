"""Acconnt endpoints"""
from __future__ import absolute_import

from flask import request
from flask_restful import Resource, fields, marshal_with
from flask_login import login_user

from app import api, db
from models.account import User
from validators.exceptions import ValidationError


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime,
}

class UserResource(Resource):

    @marshal_with(user_fields)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    @marshal_with(user_fields)
    def post(self):
        try:
            user = User(
                email=request.form.get('email', ''),
                password=request.form.get('password', '')
            )
        except ValidationError as errors:
            return {'message': errors}, 400

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return user, 201

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
