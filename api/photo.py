from flask import jsonify
from flask_restful import abort, Resource

from api.photo_parser import parser
from data import db_session
from data.photo import Gallery


def abort_if_photo_not_found(gallery_id):
    session = db_session.create_session()
    photo = session.get(Gallery, gallery_id)
    if not photo:
        abort(404, error=f"Photo {gallery_id} not found")


class PhotoResource(Resource):
    def get(self, gallery_id):
        abort_if_photo_not_found(gallery_id)
        session = db_session.create_session()
        photo = session.get(Gallery, gallery_id)
        return jsonify({'successful': 'OK',
                        'photo': photo.to_dict(
                            only=('id', 'img_path'))})

    def delete(self, gallery_id):
        abort_if_photo_not_found(gallery_id)
        session = db_session.create_session()
        photo = session.get(Gallery, gallery_id)
        session.delete(photo)
        session.commit()
        return jsonify({'successful': 'OK'})

class PhotoListResource(Resource):
    def get(self):
        session = db_session.create_session()
        photos = session.query(Gallery).all()
        print(photos)
        return jsonify({'successful': 'OK',
                        "photos": [
                            item.to_dict(only=('id', 'img_path'))
                            for item in photos]})

    def post(self):
        print(1)
        args = parser.parse_args()
        print(1)
        session = db_session.create_session()
        photo = Gallery(
            img_path=args['img_path']
        )
        session.add(photo)
        session.commit()
        return jsonify({'successful': 'OK'})
