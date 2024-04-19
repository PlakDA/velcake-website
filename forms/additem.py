from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, DateField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class AddItemForm(FlaskForm):
    status = SelectField('Статус', validators=[DataRequired()],
                         choices=[('В работе', 'В работе'), ('Готово', 'Готово'), ('Выдан', 'Выдан')])
    total = IntegerField('Цена', validators=[DataRequired()])
    client_info = TextAreaField('Информация о клиенте', validators=[DataRequired()])
    date = DateField('Дата выдачи заказа')
    submit = SubmitField('Добавить')
