import os.path
import sqlite3

import requests
from flask import Flask, make_response, jsonify, render_template, redirect, request, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api

from api import menu as menu_api
from api import orders as order_api
from api import users as users_api
from api import photo as photo_api
from data import db_session
from data.users import User
from forms.additem import AddItemForm
from forms.addmenu import AddMenuForm
from forms.addphoto import AddPhotoForm
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'velcake_secret_key'


def perform_search(query):
    # Connect to the database
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    # Execute the search query
    c.execute("SELECT * FROM menu WHERE name LIKE ?", (query,))
    results = c.fetchall()

    # Close the connection
    conn.close()
    print(results)
    return results


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
    session.clear()
    return redirect("/")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/Gallery', methods=['GET'])
def photo():

    items = requests.get('http://127.0.0.1:8080/api/photo').json()['photos']
    print(items)
    return render_template('Gallery.html', items=items)

@app.route('/photo/add', methods=['GET', 'POST'])
@login_required
def addphoto():
    form = AddPhotoForm()
    if form.validate_on_submit():
        print(requests.get('http://127.0.0.1:8080/api/photo').json())

        feature_name = "photo" + str(requests.get('http://127.0.0.1:8080/api/photo').json()["photos"][-1]["id"] + 1) + '.png'
        print(feature_name)
        requests.post('http://127.0.0.1:8080/api/photo', json={
                                                              "img_path": f'static/images/{feature_name}'})
        form.img_file.data.save(os.path.join(os.getcwd(), f'static/images/{feature_name}'))

        return redirect('/Gallery')
    return render_template('addphoto.html', form=form)


@app.route('/photo/delete/<int:id>')
@login_required
def photodelete(id):
    requests.delete(f'http://127.0.0.1:8080/api/photo/{id}')
    os.remove(f'static/images/{id}.png')
    return redirect('/Gallery')


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
        if form.org_code.data != 'org_code':
            return render_template('regist.html', form=form, message='Неправильный код организации')
        requests.post('http://127.0.0.1:8080/api/users',
                      json={"login": form.login.data, "password": form.password.data})
        return redirect('/reg')
    return render_template('regist.html', form=form)


@app.route('/menu')
def menu1():
    items = requests.get('http://127.0.0.1:8080/api/menu').json()['menu']
    return render_template('menu.html', data=items)


@app.route('/menu/add', methods=['GET', 'POST'])
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
        print(form.img_file.data)
        return redirect('/menu')
    return render_template('addmenu.html', form=form)


def formed_menus_list(menus=None):
    if not menus:
        menus = session.get('cart', [])

    menus_list = list()
    for id in set(menus):
        dish = requests.get(f'http://127.0.0.1:8080/api/menu/{id}').json()
        weight = dish["dish"]["weight"]

        position_card = dict()
        position_card['id'] = id
        position_card['name'] = (
            f'[{dish["dish"]["category"]}] {dish["dish"]["name"]} '
            f'{int(weight) if weight > 10 else weight}{"г" if weight > 10 else "л"}')
        position_card['price'] = dish["dish"]["price"]
        position_card['count'] = menus.count(id)

        menus_list.append(position_card)

    return menus_list


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', cart=formed_menus_list())


@app.route('/cart/add/<int:id>')
@login_required
def cart_add(id):
    session.modified = True
    if 'cart' not in session:
        session['cart'] = list()
    session['cart'].append(id)
    return redirect(request.referrer)


@app.route('/cart/remove/<int:id>')
@login_required
def cart_remove(id):
    session.modified = True
    session['cart'].remove(id)
    return redirect(request.referrer)


@app.route('/cart/clear')
@login_required
def cart_clear():
    session.pop('cart', None)
    return redirect('/cart')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():

    items = requests.get('http://127.0.0.1:8080/api/orders').json()['orders']
    print(items)

    for d in range(len(items)):
        ret = {}
        t = '   Название                 Количество\n\n'
        s = ''
        for i in items[d]['menus'].split():
            print(i)
            dish = requests.get(f'http://127.0.0.1:8080/api/menu/{int(i)}').json()['dish']['name']
            if dish not in ret:
                ret[dish] = 1
            else:
                ret[dish] += 1
        for key, value in ret.items():
            if value == 1:
                w = 'штука'
            elif value in [2, 3, 4]:
                w = 'штуки'
            else:
                w = 'штук'
            s += '    ' + str(key) + ' ' * (30 - len(str(key))) + str(value) + ' ' + w + '\n'
        items[d]['menus'] = s
        print(items[d]['menus'])
    return render_template('dashboard.html', data=items, t=t)


@app.route('/search/<query>', methods=['GET'])
def search(query):
    query = request.form['query']
    print(query)
    # Perform search and return results
    results = perform_search(query)
    print(results)
    return render_template('results.html', query=query, results=results)


@app.route('/orders/add', methods=['GET', 'POST'])
@login_required
def additem():
    form = AddItemForm()
    if form.validate_on_submit():
        requests.post('http://127.0.0.1:8080/api/orders', json={"status": form.status.data,
                                                           "menus": ' '.join(map(str, session.get('cart'))),
                                                           "total": form.total.data,
                                                           "client_info": form.client_info.data,
                                                           "date": str(form.date.data)})
        session.pop('cart', None)
        return redirect('/menu')

    total = 0
    order_description = 'Название ----- Количество ----- Итоговая цена\n\n'
    for el in formed_menus_list():
        order_description += f'{el["name"]} ----- {el["count"]} ----- {el["price"]}р\n'
        total += el['price']
    form.total.data = total

    return render_template('additem.html', form=form, order_description=order_description)


@app.route('/menu/delete/<int:id>')
@login_required
def menudelete(id):
    requests.delete(f'http://127.0.0.1:8080/api/menu/{id}')
    os.remove(f'static/images/{id}.png')
    return redirect('/menu')

@app.route('/dashboard/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def dashedit(id):
    form = AddItemForm()
    if request.method == 'GET':
        dish = requests.get(f'http://127.0.0.1:8080/api/orders/{id}').json()
        print(dish)
        form.status.data = dish["order"]["status"]
        form.client_info.data = dish["order"]["client_info"]

        return render_template('orderedit.html', form=form)

    if request.method == 'POST':
        requests.put(f'http://127.0.0.1:8080/api/orders/{id}', json={
            "status": form.status.data,
            "client_info": form.client_info.data,
            "date": str(form.date.data)
        })

        return redirect('/dashboard')


@app.route('/dashboard/delete/<int:id>')
@login_required
def dashdel(id):
    requests.delete(f'http://127.0.0.1:8080/api/orders/{id}')
    return redirect('/dashboard')


@app.route('/menu/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def menuedit(id):
    form = AddMenuForm()
    if request.method == 'GET':
        dish = requests.get(f'http://127.0.0.1:8080/api/menu/{id}').json()
        form.name.data = dish["dish"]["name"]
        form.category.data = dish["dish"]["category"]
        form.description.data = dish["dish"]["description"]
        form.weight.data = dish["dish"]["weight"]
        form.price.data = dish["dish"]["price"]
        return render_template('menuedit.html', form=form)

    if request.method == 'POST':
        requests.put(f'http://127.0.0.1:8080/api/menu/{id}', json={
            "name": form.name.data,
            "category": form.category.data,
            "description": form.description.data,
            "weight": float(form.weight.data),
            "price": form.price.data
        })
        if form.img_file.data:
            form.img_file.data.save(os.path.join(os.getcwd(), f'static/images/{id}.png'))
        return redirect('/menu')


def api_connect():
    api.add_resource(menu_api.MenuResource, '/api/menu/<int:dish_id>')
    api.add_resource(menu_api.MenuListResource, '/api/menu')
    api.add_resource(order_api.OrderResource, '/api/orders/<int:order_id>')
    api.add_resource(order_api.OrderListResource, '/api/orders')
    api.add_resource(users_api.UserResource, '/api/users/<int:user_id>')
    api.add_resource(users_api.UserListResource, '/api/users')
    api.add_resource(photo_api.PhotoResource, '/api/photo/<int:gallery_id>')
    api.add_resource(photo_api.PhotoListResource, '/api/photo')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    api_connect()
    app.run('127.0.0.1', port=8080)
