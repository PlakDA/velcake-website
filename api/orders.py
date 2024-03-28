from flask import jsonify
from flask_restful import abort, Resource

from api.orders_parser import put_parser, parser
from data import db_session
from data.orders import Order


def abort_if_order_not_found(order_id):
    session = db_session.create_session()
    order = session.get(Order, order_id)
    if not order:
        abort(404, error=f"Order {order_id} not found")


class OrderResource(Resource):
    def get(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.get(Order, order_id)
        return jsonify({'successful': 'OK',
                        'order': order.to_dict(only=('id', 'status', 'menus', 'total', 'client_info'))})

    def delete(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.get(Order, order_id)
        session.delete(order)
        session.commit()
        return jsonify({'successful': 'OK'})

    def put(self, order_id):
        abort_if_order_not_found(order_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        order = session.get(Order, order_id)
        order.status = args['status'] if args['status'] else order.status
        order.menus = args['menus'] if args['menus'] else order.menus
        order.total = args['total'] if args['total'] else order.total
        order.client_info = args['client_info'] if args['client_info'] else order.client_info
        session.add(order)
        session.commit()
        return jsonify({'successful': 'OK'})


class OrderListResource(Resource):
    def get(self):
        session = db_session.create_session()
        orders = session.query(Order).all()
        return jsonify({'successful': 'OK',
                        'orders': [item.to_dict(only=('id', 'status', 'menus', 'total', 'client_info'))
                                   for item in orders]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        order = Order(
            status=args['status'],
            menus=args['menus'],
            total=args['total'],
            client_info=args['client_info']
        )
        session.add(order)
        session.commit()
        return jsonify({'successful': 'OK'})
