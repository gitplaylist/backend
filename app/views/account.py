"""Acconnt endpoints"""
from __future__ import absolute_import

from flask import request
from flask_restful import fields, marshal, Resource
from flask_login import login_user

from app import api, db
from models.account import User
from exceptions import ValidationError


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime,
}

class UserResource(Resource):
    """Define user RESTful endpoints."""

    def get(self, user_id):
        """Serve GET requests."""
        user = User.query.get_or_404(user_id)
        return marshal(user, user_fields)

    def post(self):
        """Serve POST requests."""
        try:
            user = User(
                email=request.form.get('email', ''),
                password=request.form.get('password', '')
            )
        except ValidationError as error:
            return {'errors': error.message}, 400

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return marshal(user, user_fields), 201

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
