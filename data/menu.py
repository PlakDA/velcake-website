import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Dish(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'menu'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    img_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
