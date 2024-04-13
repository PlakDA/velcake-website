from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('category', required=True)
parser.add_argument('description', required=True)
parser.add_argument('weight', type=float, required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('img_path', required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('name')
put_parser.add_argument('category')
put_parser.add_argument('description')
put_parser.add_argument('weight', type=float)
put_parser.add_argument('price', type=int)
