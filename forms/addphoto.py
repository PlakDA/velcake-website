from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.fields.simple import SubmitField


class AddPhotoForm(FlaskForm):

    img_file = FileField('Картинка')
    submit = SubmitField('Добавить')