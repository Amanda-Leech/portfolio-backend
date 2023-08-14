from flask import jsonify, Request, Response
from db import db
from util.reflection import populate_object
from model.resume import Resume, resume_schema, resumes_schema


#create resume
def resume_add(req: Request) -> Response:
    post_data = req.get_json()
    if post_data:
        resume_title = post_data.get('resume_title')
        resume_info = post_data.get('resume_info')
        active = post_data.get("active")
        new_resume = Resume.get_new_resume()
        populate_object(new_resume, post_data)
        db.session.add(new_resume)
        db.session.commit()
        return jsonify({"message": "resume created", "resume": resume_schema.dump(new_resume)}), 201
    return jsonify({"message": 'no data'}), 404

#read resume one
def resume_get_by_id(req: Request, resume_id) -> Response:
    resume_id = resume_id.strip()
    resume_data = db.session.query(Resume).filter(
        Resume.resume_id == resume_id).first()
    if resume_data:
        resume_dict = resume_schema.dump(resume_data)
        return jsonify([resume_dict]), 200
    return jsonify({"message":'You do not have this resume'}), 404

#read all
def resume_get_all(req: Request) -> Response:
    all_resumes = db.session.query(Resume).all()
    resume_list = resumes_schema.dump(all_resumes)
    return jsonify(resume_list), 200

#update resume
def resume_update(req: Request, resume_id) -> Response:
    post_data = req.get_json()
    if post_data:
        resume_title = post_data.get('resume_title')
        resume_info = post_data.get('resume_info')
        active = post_data.get("active")
        resume_data = db.session.query(Resume).filter(
            Resume.resume_id == resume_id).first()
        populate_object(resume_data, post_data)
        db.session.commit()
        return jsonify({"message": "resume updated", "resume": resume_schema.dump(resume_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete resume
def resume_delete(req: Request, resume_id) -> Response:
    resume_data = db.session.query(Resume).filter(
        Resume.resume_id == resume_id).first()
    if resume_data:
        db.session.delete(resume_data)
        db.session.commit()
        return jsonify({"message":'Resume deleted'}), 200
    return jsonify({"message":'You don\'t have this resume'}), 404

#archive resume
def resume_archive(req: Request, resume_id) -> Response:
    resume_data = db.session.query(Resume).filter(Resume.resume_id == resume_id).first()
    if resume_data:
        resume_data.active = not resume_data.active
        db.session.commit()
        return jsonify({"message": "resume archive updated", "resume": resume_schema.dump(resume_data)}), 200
    return jsonify({"message": "You don't have this resume"}), 404
