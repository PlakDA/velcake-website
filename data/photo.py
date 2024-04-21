import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Gallery(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'photo'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    img_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)