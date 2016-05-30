from flask_restful import Resource, fields, marshal_with, reqparse

from app import api
from models.account import User


def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    return email_str
    # if valid_email(email_str):
    #     return email_str
    # else:
    #     raise ValueError('{} is not a valid email'.format(email_str))

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'username', dest='username',
    location='form', required=True,
    help='The user\'s username',
)
post_parser.add_argument(
    'email', dest='email',
    type=email, location='form',
    required=True, help='The user\'s email',
)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime,
}


class UserResource(Resource):

    @marshal_with(user_fields)
    def post(self):
        args = post_parser.parse_args()
        user = User(args.eamil, args.password)
        return user

    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

api.add_resource(User, '/users')
