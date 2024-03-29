from flask import Flask, make_response, jsonify, render_template
from flask_restful import Api
from flask_login import LoginManager
import requests


from api import menu as menu_api
from api import orders as order_api
from api import users as users_api
from data import db_session



app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'velcake_secret_key'

login_manager = LoginManager(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/gallery')
def photo():
    return render_template('Gallery.html')


@app.route('/reg')
def reg():
    return render_template('reg.html')


@app.route('/regist')
def regist():
    return render_template('regist.html')


@app.route('/menu')
def menu1():
    items = requests.get('http://127.0.0.1:8080/api/menu').json()['menu']
    return render_template('menu.html', data=items)


def api_connect():
    api.add_resource(menu_api.MenuResource, '/api/menu/<int:dish_id>')
    api.add_resource(menu_api.MenuListResource, '/api/menu')
    api.add_resource(order_api.OrderResource, '/api/orders/<int:order_id>')
    api.add_resource(order_api.OrderListResource, '/api/orders')
    api.add_resource(users_api.UserResource, '/api/users/<int:user_id>')
    api.add_resource(users_api.UserListResource, '/api/users')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    api_connect()
    app.run('127.0.0.1', port=8080)
