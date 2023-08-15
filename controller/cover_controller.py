from flask import jsonify, Request, Response
from db import db
from util.reflection import populate_object
from model.cover import Cover, cover_schema, covers_schema
def cover_add(req: Request) -> Response:
    post_data = req.get_json()
    if post_data:
        cover_title = post_data.get('cover_title')
        cover_info = post_data.get('cover_info')
        active = post_data.get("active")
        new_cover = Cover.get_new_cover()
        populate_object(new_cover, post_data)
        db.session.add(new_cover)
        db.session.commit()
        return jsonify([cover_schema.dump(new_cover)]), 201
    return jsonify({"message": 'no data'}), 404

#read cover one title
def cover_get_by_cover_title(req: Request, cover_title) -> Response:
    cover_title = cover_title.strip()
    cover_data = db.session.query(Cover).filter(
        Cover.cover_title == cover_title).first()
    if cover_data:
        cover_dict = cover_schema.dump(cover_data)
        return jsonify([cover_dict]), 200
    return jsonify({"message":'You do not have this cover'}), 404

#read cover one id
def cover_get_by_id(req: Request, cover_id) -> Response:
    cover_id = cover_id.strip()
    cover_data = db.session.query(Cover).filter(
        Cover.cover_id == cover_id).first()
    if cover_data:
        cover_dict = cover_schema.dump(cover_data)
        return jsonify([cover_dict]), 200
    return jsonify({"message":'You do not have this cover'}), 404


#read all
def cover_get_all(req: Request) -> Response:
    all_covers = db.session.query(Cover).all()
    cover_list = covers_schema.dump(all_covers)
    return jsonify(cover_list), 200

#update cover
def cover_update(req: Request, cover_id) -> Response:
    post_data = req.get_json()
    if post_data:
        cover_title = post_data.get('cover_title')
        cover_info = post_data.get('cover_info')
        active = post_data.get("active")
        cover_data = db.session.query(Cover).filter(
            Cover.cover_id == cover_id).first()
        if not cover_data:
            return jsonify({"message": "cover not found"}), 404
        populate_object(cover_data, post_data)
        db.session.commit()
        return jsonify([cover_schema.dump(cover_data)]), 200
    return jsonify({"message": "no data"}), 404

#delete cover
def cover_delete(req: Request, cover_id) -> Response:
    cover_data = db.session.query(Cover).filter(
        Cover.cover_id == cover_id).first()
    if cover_data:
        db.session.delete(cover_data)
        db.session.commit()
        return jsonify({"message":'Cover deleted'}), 200
    return jsonify({"message":'You don\'t have this cover'}), 404

#archive cover
def cover_archive(req: Request, cover_id) -> Response:
    cover_data = db.session.query(Cover).filter(Cover.cover_id == cover_id).first()
    if cover_data:
        cover_data.active = not cover_data.active
        db.session.commit()
        return jsonify({cover_schema.dump(cover_data)}), 200
    return jsonify({"message": "You don't have this cover"}), 404
