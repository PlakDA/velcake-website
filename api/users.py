from flask import jsonify
from flask_restful import abort, Resource
from werkzeug.security import generate_password_hash

from api.users_parser import parser, put_parser
from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.get(User, user_id)
    if not users:
        abort(404, error=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        return jsonify({'successful': 'OK',
                        'user': user.to_dict(only=('id', 'login', 'password', 'name'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'successful': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        user = session.get(User, user_id)
        user.login = args['login'] if args['login'] else user.login
        user.password = generate_password_hash(args['password']) if args['password'] else user.password
        user.name = args['name'] if args['name'] else user.name
        session.add(user)
        session.commit()
        return jsonify({'successful': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'successful': 'OK',
                        'users': [item.to_dict(only=('id', 'login', 'password', 'name'))
                                  for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            login=args['login'],
            password=generate_password_hash(args['password']),
            name=args['name']
        )
        session.add(user)
        session.commit()
        return jsonify({'successful': 'OK'})
