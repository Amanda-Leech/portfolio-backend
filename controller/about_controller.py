from flask import jsonify, Request, Response
from db import db
from util.reflection import populate_object
from model.about import About, about_schema, abouts_schema


#create about
def about_add(req: Request) -> Response:
    post_data = req.get_json()
    if post_data:
        about_title = post_data.get('about_title')
        about_info = post_data.get('about_info')
        active = post_data.get("active")
        new_about = About.get_new_about()
        populate_object(new_about, post_data)
        db.session.add(new_about)
        db.session.commit()
        return jsonify([about_schema.dump(new_about)]), 200
    return jsonify({"message": 'no data'}), 404

#read one
def about_get_by_title(req: Request, about_title) -> Response:
    about_title = about_title.strip()
    about_data = db.session.query(About).filter(
        About.about_title == about_title).first()
    if about_data:
        about_dict = about_schema.dump(about_data)
        return jsonify([about_dict]), 200
    return jsonify({"message":'You do not have this about'}), 404

#read all
def about_get_all(req: Request) -> Response:
    all_abouts = db.session.query(About).all()
    about_list = abouts_schema.dump(all_abouts)
    return jsonify([about_list]), 200

#update by id
def about_update_id(req: Request, about_id) -> Response:
    post_data = req.get_json()
    if post_data:
        about_title = post_data.get('about_title')
        about_info = post_data.get('about_info')
        active = post_data.get("active")
        about_data = db.session.query(About).filter(
            About.about_id == about_id).first()
        populate_object(about_data, post_data)
        db.session.commit()
        return jsonify([about_schema.dump(about_data)]), 200
    return jsonify({"message": "no data"}), 404


#update about
def about_update(req: Request, about_title) -> Response:
    post_data = req.get_json()
    if post_data:
        about_title = post_data.get('about_title')
        about_info = post_data.get('about_info')
        active = post_data.get("active")
        about_data = db.session.query(About).filter(
            About.about_title == about_title).first()
        populate_object(about_data, post_data)
        db.session.commit()
        return jsonify([about_schema.dump(about_data)]), 200
    return jsonify({"message": "no data"}), 404

#delete about
def about_delete(req: Request, about_id) -> Response:
    about_data = db.session.query(About).filter(
        About.about_id == about_id).first()
    if about_data:
        db.session.delete(about_data)
        db.session.commit()
        return jsonify({"message":'About deleted'}), 200
    return jsonify({"message":'You don\'t have this about'}), 404

#archive about
def about_archive(req: Request, about_id) -> Response:
    about_data = db.session.query(About).filter(About.about_id == about_id).first()
    if about_data:
        about_data.active = not about_data.active
        db.session.commit()
        return jsonify([about_schema.dump(about_data)]), 200
    return jsonify({"message": "You don't have this about"}), 404
