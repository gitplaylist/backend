from app import db, api
from models.account import User

from flask_restful import fields, marshal_with, reqparse, Resource


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
    location='form', equired=True,
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


class User(Resource):

    @marshal_with(user_fields)
    def post(self):
        args = post_parser.parse_args()
        user = User(args.username, args.email)
        return user

    @marshal_with(user_fields)
    def get(self, user_id):
        args = post_parser.parse_args()
        user = get_or_abort(User, user_id)
        return user

api.add_resource(User, '/users')
