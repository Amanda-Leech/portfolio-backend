from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.education import Education, education_schema, educations_schema


#create education
@authenticate_return_auth
def education_add(req: Request,auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        school_name = post_data.get('school_name')
        certificate = post_data.get('certificate')
        date_obtained = post_data.get('date_obtained')
        active = post_data.get("active")

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "not authorized"}), 401

        if not certificate:
            return jsonify({"message" : "Certificate name required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        new_education = Education.get_new_education()

        populate_object(new_education, post_data)

        db.session.add(new_education)
        db.session.commit()

        return jsonify({"message": "education created", "education": education_schema.dump(new_education)}), 201
    return jsonify({"message": 'no data'}), 404

#read education one
def education_get_by_id(req: Request, education_id) -> Response:
    education_id = education_id.strip()

    if validate_uuid4(education_id) == False:
        return jsonify({"message": "invalid education id"}), 400

    education_data = db.session.query(Education).filter(
        Education.education_id == education_id).first()

    if education_data:
        education_dict = education_schema.dump(education_data)

        return jsonify({"message": "success", "education": education_dict}), 200

    return jsonify({"message":'You do not have this education'}), 404

#read all
def education_get_all(req: Request) -> Response:
    all_educations = db.session.query(Education).all()
    education_list = educations_schema.dump(all_educations)

    return jsonify(education_list), 200

#update education
@authenticate_return_auth
def education_update(req: Request, education_id, auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        school_name = post_data.get('school_name')
        certificate = post_data.get('certificate')
        date_obtained = post_data.get('date_obtained')
        active = post_data.get("active")

        if validate_uuid4(education_id) == False:
            return jsonify({"message": "invalid education id"}), 400

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "unauthorized"}), 401

        education_data = db.session.query(Education).filter(
            Education.education_id == education_id).first()
        
        if bool(certificate)==False:
            if certificate == "":
                return jsonify({"message" : "Certification name required"}), 400
          
        if not education_data:
            return jsonify({"message": "education not found"}), 404

        if education_id:
            if not validate_uuid4(education_id):
                return jsonify({"message": "invalid education id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(education_data, post_data)
        db.session.commit()

        return jsonify({"message": "education updated", "education": education_schema.dump(education_data)}), 200
    return jsonify({"message": "no education"}), 404

#delete education
@authenticate_return_auth
def education_delete(req: Request, education_id, auth_info) -> Response:
    if validate_uuid4(education_id) == False:
        return jsonify({"message": "invalid education id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    education_data = db.session.query(Education).filter(
        Education.education_id == education_id).first()

    if education_data:
        db.session.delete(education_data)
        db.session.commit()

        return jsonify({"message":'Education deleted'}), 200

    return jsonify({"message":'You don\'t have this education'}), 404

#activity education
@authenticate_return_auth
def education_activity(req: Request, education_id, auth_info) -> Response:
    if not validate_uuid4(education_id):
        return jsonify({"message": "invalid education id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        education_data = db.session.query(Education).filter(Education.education_id == education_id).first()

    if education_data:
        education_data.active = not education_data.active
        db.session.commit()

        return jsonify({"message": "education activity updated", "education": education_schema.dump(education_data)}), 200
    return jsonify({"message": "You don't have this education"}), 404
