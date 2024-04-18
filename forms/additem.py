from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FileField, DecimalField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class AddItemForm(FlaskForm):
    status = StringField('Статус', validators=[DataRequired()])
    menus = TextAreaField('Заказанные блюда')
    total = IntegerField('Цена', validators=[DataRequired()])
    client_info = TextAreaField('Информация о клиенте')
    time = TextAreaField('Дата выдачи заказа')
    submit = SubmitField('Добавить')
