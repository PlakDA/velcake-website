from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('password', required=True)
parser.add_argument('name', required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('login')
put_parser.add_argument('password')
put_parser.add_argument('name')
