from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.cover import Cover, cover_schema, covers_schema


#create cover
@authenticate_return_auth
def cover_add(req: Request,auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        cover_title = post_data.get('cover_title')
        cover_info = post_data.get('cover_info')
        active = post_data.get("active")

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "not authorized"}), 401

        if not cover_title or not cover_info:
            return jsonify({"message" : "Cover and use required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        new_cover = Cover.get_new_cover()

        populate_object(new_cover, post_data)

        db.session.add(new_cover)
        db.session.commit()

        return jsonify({"message": "cover created", "cover": cover_schema.dump(new_cover)}), 201

    return jsonify({"message": 'no data'}), 404

#read cover one
def cover_get_by_cover_title(req: Request, cover_title) -> Response:
    cover_title = cover_title.strip()

    # if validate_uuid4(cover_id) == False:
    #     return jsonify({"message": "invalid cover id"}), 400

    cover_data = db.session.query(Cover).filter(
        Cover.cover_title == cover_title).first()

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
# @authenticate_return_auth
def cover_update(req: Request, cover_title) -> Response:
    post_data = req.get_json()

    if post_data:
        cover_title = post_data.get('cover_title')
        cover_info = post_data.get('cover_info')
        active = post_data.get("active")

        # if validate_uuid4(cover_id) == False:
        #     return jsonify({"message": "invalid cover id"}), 400

        # if auth_info.user.role not in ["admin"]:
        #     return jsonify({"message": "unauthorized"}), 401

        cover_data = db.session.query(Cover).filter(
            Cover.cover_title == cover_title).first()
        
        if bool(cover_title)== False or bool(cover_info)==False:
            if cover_title== "" or cover_info == "":
                return jsonify({"message" : "Cover and info required"}), 400
          
        if not cover_data:
            return jsonify({"message": "cover not found"}), 404

        # if cover_id:
        #     if not validate_uuid4(cover_id):
        #         return jsonify({"message": "invalid cover id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(cover_data, post_data)
        db.session.commit()

        return jsonify({"message": "cover updated", "cover": cover_schema.dump(cover_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete cover
@authenticate_return_auth
def cover_delete(req: Request, cover_id, auth_info) -> Response:
    if validate_uuid4(cover_id) == False:
        return jsonify({"message": "invalid cover id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "uUnauthorized"}), 403

    cover_data = db.session.query(Cover).filter(
        Cover.cover_id == cover_id).first()

    if cover_data:
        db.session.delete(cover_data)
        db.session.commit()

        return jsonify({"message":'Cover deleted'}), 200

    return jsonify({"message":'You don\'t have this cover'}), 404

#archive cover
@authenticate_return_auth
def cover_archive(req: Request, cover_id, auth_info) -> Response:
    if not validate_uuid4(cover_id):
        return jsonify({"message": "invalid cover id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        cover_data = db.session.query(Cover).filter(Cover.cover_id == cover_id).first()

    if cover_data:
        cover_data.active = not cover_data.active
        db.session.commit()

        return jsonify({"message": "cover archive updated", "cover": cover_schema.dump(cover_data)}), 200
    return jsonify({"message": "You don't have this cover"}), 404
