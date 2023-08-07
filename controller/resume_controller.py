from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.resume import Resume, resume_schema, resumes_schema


#create resume
@authenticate_return_auth
def resume_add(req: Request,auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        resume_title = post_data.get('resume_title')
        resume_info = post_data.get('resume_info')
        active = post_data.get("active")

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "Unauthorized"}), 401

        if not resume_title or not resume_info:
            return jsonify({"message" : "Resume and use required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        new_resume = Resume.get_new_resume()

        populate_object(new_resume, post_data)

        db.session.add(new_resume)
        db.session.commit()

        return jsonify({"message": "resume created", "resume": resume_schema.dump(new_resume)}), 201
    return jsonify({"message": 'no data'}), 404

#read resume one
def resume_get_by_id(req: Request, resume_id) -> Response:
    resume_id = resume_id.strip()

    if validate_uuid4(resume_id) == False:
        return jsonify({"message": "invalid resume id"}), 400

    resume_data = db.session.query(Resume).filter(
        Resume.resume_id == resume_id).first()

    if resume_data:
        resume_dict = resume_schema.dump(resume_data)

        return jsonify({"message": "success", "resume": resume_dict}), 200

    return jsonify({"message":'You do not have this resume'}), 404

#read all
def resume_get_all(req: Request) -> Response:
    all_resumes = db.session.query(Resume).all()
    resume_list = resumes_schema.dump(all_resumes)

    return jsonify(resume_list), 200

#update resume
@authenticate_return_auth
def resume_update(req: Request, resume_id, auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        resume_title = post_data.get('resume_title')
        resume_info = post_data.get('resume_info')
        active = post_data.get("active")

        if validate_uuid4(resume_id) == False:
            return jsonify({"message": "invalid resume id"}), 400

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "unauthorized"}), 401

        resume_data = db.session.query(Resume).filter(
            Resume.resume_id == resume_id).first()
        
        if bool(resume_title)== False or bool(resume_info)==False:
            if resume_title== "" or resume_info == "":
                return jsonify({"message" : "Resume and use required"}), 400
          
        if not resume_data:
            return jsonify({"message": "resume not found"}), 404

        if resume_id:
            if not validate_uuid4(resume_id):
                return jsonify({"message": "invalid resume id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(resume_data, post_data)
        db.session.commit()

        return jsonify({"message": "resume updated", "resume": resume_schema.dump(resume_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete resume
@authenticate_return_auth
def resume_delete(req: Request, resume_id, auth_info) -> Response:
    if validate_uuid4(resume_id) == False:
        return jsonify({"message": "invalid resume id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "uUnauthorized"}), 403

    resume_data = db.session.query(Resume).filter(
        Resume.resume_id == resume_id).first()

    if resume_data:
        db.session.delete(resume_data)
        db.session.commit()

        return jsonify({"message":'Resume deleted'}), 200

    return jsonify({"message":'You don\'t have this resume'}), 404

#activity resume
@authenticate_return_auth
def resume_activity(req: Request, resume_id, auth_info) -> Response:
    if not validate_uuid4(resume_id):
        return jsonify({"message": "invalid resume id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        resume_data = db.session.query(Resume).filter(Resume.resume_id == resume_id).first()

    if resume_data:
        resume_data.active = not resume_data.active
        db.session.commit()

        return jsonify({"message": "resume activity updated", "resume": resume_schema.dump(resume_data)}), 200
    return jsonify({"message": "You don't have this resume"}), 404
