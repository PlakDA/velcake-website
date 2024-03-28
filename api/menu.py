from flask import jsonify
from flask_restful import abort, Resource

from api.menu_parser import put_parser, parser
from data import db_session
from data.menu import Dish


def abort_if_dish_not_found(dish_id):
    session = db_session.create_session()
    dish = session.get(Dish, dish_id)
    if not dish:
        abort(404, error=f"Menu position {dish_id} not found")


class MenuResource(Resource):
    def get(self, dish_id):
        abort_if_dish_not_found(dish_id)
        session = db_session.create_session()
        dish = session.get(Dish, dish_id)
        return jsonify({'successful': 'OK',
                        'dish': dish.to_dict(
                            only=('id', 'name', 'category', 'description', 'weight', 'price', 'img_path'))})

    def delete(self, dish_id):
        abort_if_dish_not_found(dish_id)
        session = db_session.create_session()
        dish = session.get(Dish, dish_id)
        session.delete(dish)
        session.commit()
        return jsonify({'successful': 'OK'})

    def put(self, dish_id):
        abort_if_dish_not_found(dish_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        dish = session.get(Dish, dish_id)
        dish.name = args['name'] if args['name'] else dish.name
        dish.category = args['category'] if args['category'] else dish.category
        dish.description = args['description'] if args['description'] else dish.description
        dish.weight = args['weight'] if args['weight'] else dish.weight
        dish.price = args['price'] if args['price'] else dish.price
        dish.img_path = args['img_path'] if args['img_path'] else dish.img_path
        session.add(dish)
        session.commit()
        return jsonify({'successful': 'OK'})


class MenuListResource(Resource):
    def get(self):
        session = db_session.create_session()
        menu = session.query(Dish).all()
        return jsonify({'successful': 'OK',
                        'menu': [
                            item.to_dict(only=('id', 'name', 'category', 'description', 'weight', 'price', 'img_path'))
                            for item in menu]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        dish = Dish(
            name=args['name'],
            category=args['category'],
            description=args['description'],
            weight=args['weight'],
            price=args['price'],
            img_path=args['img_path']
        )
        session.add(dish)
        session.commit()
        return jsonify({'successful': 'OK'})
