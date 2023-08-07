from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.about import About, about_schema, abouts_schema


#create about
@authenticate_return_auth
def about_add(req: Request,auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        about_title = post_data.get('about_title')
        about_info = post_data.get('about_info')
        active = post_data.get("active")

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "not authorized"}), 401

        if not about_title or not about_info:
            return jsonify({"message" : "Title and info required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        new_about = About.get_new_about()

        populate_object(new_about, post_data)

        db.session.add(new_about)
        db.session.commit()

        return jsonify({"message": "about created", "about": about_schema.dump(new_about)}), 201
    return jsonify({"message": 'no data'}), 404

#read about one
def about_get_by_id(req: Request, about_id) -> Response:
    about_id = about_id.strip()

    if validate_uuid4(about_id) == False:
        return jsonify({"message": "invalid about id"}), 400

    about_data = db.session.query(About).filter(
        About.about_id == about_id).first()

    if about_data:
        about_dict = about_schema.dump(about_data)

        return jsonify(about_dict), 200

    return jsonify({"message":'You do not have this about'}), 404

#read all
def about_get_all(req: Request) -> Response:
    all_abouts = db.session.query(About).all()
    about_list = abouts_schema.dump(all_abouts)

    return jsonify(about_list), 200

#update about
@authenticate_return_auth
def about_update(req: Request, about_id, auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        about_title = post_data.get('about_title')
        about_info = post_data.get('about_info')
        active = post_data.get("active")

        if validate_uuid4(about_id) == False:
            return jsonify({"message": "invalid about id"}), 400

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "unauthorized"}), 401

        about_data = db.session.query(About).filter(
            About.about_id == about_id).first()
        
        if bool(about_title)== False or bool(about_info)==False:
            if about_title== "" or about_info == "":
                return jsonify({"message" : "About and use required"}), 400
          
        if not about_data:
            return jsonify({"message": "about not found"}), 404

        if about_id:
            if not validate_uuid4(about_id):
                return jsonify({"message": "invalid about id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(about_data, post_data)
        db.session.commit()

        return jsonify({"message": "about updated", "about": about_schema.dump(about_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete about
@authenticate_return_auth
def about_delete(req: Request, about_id, auth_info) -> Response:
    if validate_uuid4(about_id) == False:
        return jsonify({"message": "invalid about id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "uUnauthorized"}), 403

    about_data = db.session.query(About).filter(
        About.about_id == about_id).first()

    if about_data:
        db.session.delete(about_data)
        db.session.commit()

        return jsonify({"message":'About deleted'}), 200

    return jsonify({"message":'You don\'t have this about'}), 404

#activity about
@authenticate_return_auth
def about_activity(req: Request, about_id, auth_info) -> Response:
    if not validate_uuid4(about_id):
        return jsonify({"message": "invalid about id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        about_data = db.session.query(About).filter(About.about_id == about_id).first()

    if about_data:
        about_data.active = not about_data.active
        db.session.commit()

        return jsonify({"message": "about activity updated", "about": about_schema.dump(about_data)}), 200
    return jsonify({"message": "You don't have this about"}), 404
