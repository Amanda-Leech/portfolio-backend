from flask import jsonify, Request, Response
from db import db
from util.reflection import populate_object
from model.education import Education, education_schema, educations_schema


#create education
def education_add(req: Request) -> Response:
    post_data = req.get_json()
    if post_data:
        school_name = post_data.get('school_name')
        certificate = post_data.get('certificate')
        date_obtained = post_data.get('date_obtained')
        active = post_data.get("active")
        new_education = Education.get_new_education()
        populate_object(new_education, post_data)
        db.session.add(new_education)
        db.session.commit()
        return jsonify([education_schema.dump(new_education)]), 201
    return jsonify({"message": 'no data'}), 404

#read education one
def education_get_by_id(req: Request, education_id) -> Response:
    education_id = education_id.strip()
    education_data = db.session.query(Education).filter(
        Education.education_id == education_id).first()
    if education_data:
        education_dict = education_schema.dump(education_data)
        return jsonify([education_dict]), 200
    return jsonify({"message":'You do not have this education'}), 404

#read all
def education_get_all(req: Request) -> Response:
    all_educations = db.session.query(Education).all()
    education_list = educations_schema.dump(all_educations)
    return jsonify(education_list), 200

#update education
def education_update(req: Request, education_id) -> Response:
    post_data = req.get_json()
    if post_data:
        school_name = post_data.get('school_name')
        certificate = post_data.get('certificate')
        date_obtained = post_data.get('date_obtained')
        active = post_data.get("active")
        education_data = db.session.query(Education).filter(
            Education.education_id == education_id).first()
        populate_object(education_data, post_data)
        db.session.commit()
        return jsonify([education_schema.dump(education_data)]), 200
    return jsonify({"message": "no education"}), 404

#delete education
def education_delete(req: Request, education_id) -> Response:
    education_data = db.session.query(Education).filter(
        Education.education_id == education_id).first()
    if education_data:
        db.session.delete(education_data)
        db.session.commit()
        return jsonify({"message":'Education deleted'}), 200
    return jsonify({"message":'You don\'t have this education'}), 404

#archive education
def education_archive(req: Request, education_id) -> Response:
    education_data = db.session.query(Education).filter(Education.education_id == education_id).first()
    if education_data:
        education_data.active = not education_data.active
        db.session.commit()
        return jsonify([education_schema.dump(education_data)]), 200
    return jsonify({"message": "You don't have this education"}), 404
