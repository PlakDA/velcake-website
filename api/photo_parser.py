from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('img_path', required=True)


