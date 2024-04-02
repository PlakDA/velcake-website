from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FileField, DecimalField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class AddMenuForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    category = SelectField('Категория',
                           choices=[('Еда', 'Еда'), ('Чай без чая', 'Чай без чая'),
                                    ('Молочные коктейли', 'Молочные коктейли'), ('Классика', 'Классика'),
                                    ('Авторский кофе', 'Авторский кофе'), ('Раф', 'Раф'), ('Некофе', 'Некофе'),
                                    ('Чай', 'Чай')], validators=[DataRequired()])
    description = TextAreaField('Описание')
    weight = DecimalField('Вес/Объём', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    img_file = FileField('Картинка')
    submit = SubmitField('Добавить')
