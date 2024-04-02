import os.path

import requests
from flask import Flask, make_response, jsonify, render_template, redirect
from flask import request as flask_request
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api

from api import menu as menu_api
from api import orders as order_api
from api import users as users_api
from data import db_session
from data.users import User
from forms.addmenu import AddMenuForm
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'velcake_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/gallery')
def photo():
    return render_template('Gallery.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('reg.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('reg.html', form=form)


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('regist.html', form=form)


@app.route('/menu')
def menu1():
    items = requests.get('http://127.0.0.1:8080/api/menu').json()['menu']
    return render_template('menu.html', data=items)


@app.route('/addmenu', methods=['GET', 'POST'])
@login_required
def addmenu():
    form = AddMenuForm()
    if form.validate_on_submit():
        feature_name = str(requests.get('http://127.0.0.1:8080/api/menu').json()["menu"][-1]["id"] + 1) + '.png'
        requests.post('http://127.0.0.1:8080/api/menu', json={"name": form.name.data,
                                                          "category": form.category.data,
                                                          "description": form.description.data,
                                                          "weight": float(form.weight.data),
                                                          "price": form.price.data,
                                                          "img_path": f'static/images/{feature_name}'})
        form.img_file.data.save(os.path.join(os.getcwd(), f'static/images/{feature_name}'))
        return redirect('/')
    return render_template('addmenu.html', form=form)


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
