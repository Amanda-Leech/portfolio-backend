from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.skill import Skill, skill_schema, skills_schema


#create skill
@authenticate_return_auth
def skill_add(req: Request,auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        skill_name = post_data.get('skill_name')
        skill_use = post_data.get('skill_use')
        active = post_data.get("active")

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "not authorized"}), 401

        if not skill_name or not skill_use:
            return jsonify({"message" : "Skill and use required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        new_skill = Skill.get_new_skill()

        populate_object(new_skill, post_data)

        db.session.add(new_skill)
        db.session.commit()

        return jsonify({"message": "skill created", "skill": skill_schema.dump(new_skill)}), 201
    return jsonify({"message": 'no data'}), 404

#read skill one
def skill_get_by_id(req: Request, skill_id) -> Response:
    skill_id = skill_id.strip()

    if validate_uuid4(skill_id) == False:
        return jsonify({"message": "invalid skill id"}), 400

    skill_data = db.session.query(Skill).filter(
        Skill.skill_id == skill_id).first()

    if skill_data:
        skill_dict = skill_schema.dump(skill_data)

        return jsonify({"message": "success", "skill": skill_dict}), 200

    return jsonify({"message":'You do not have this skill'}), 404

#read all
def skill_get_all(req: Request) -> Response:
    all_skills = db.session.query(Skill).all()
    skill_list = skills_schema.dump(all_skills)

    return jsonify(skill_list), 200

#update skill
@authenticate_return_auth
def skill_update(req: Request, skill_id, auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        skill_name = post_data.get('skill_name')
        skill_use = post_data.get('skill_use')
        active = post_data.get("active")

        if validate_uuid4(skill_id) == False:
            return jsonify({"message": "invalid skill id"}), 400

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "unauthorized"}), 401

        skill_data = db.session.query(Skill).filter(
            Skill.skill_id == skill_id).first()
        
        if bool(skill_name)== False or bool(skill_use)==False:
            if skill_name== "" or skill_use == "":
                return jsonify({"message" : "Skill and use required"}), 400
          
        if not skill_data:
            return jsonify({"message": "skill not found"}), 404

        if skill_id:
            if not validate_uuid4(skill_id):
                return jsonify({"message": "invalid skill id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(skill_data, post_data)
        db.session.commit()

        return jsonify({"message": "skill updated", "skill": skill_schema.dump(skill_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete skill
@authenticate_return_auth
def skill_delete(req: Request, skill_id, auth_info) -> Response:
    if validate_uuid4(skill_id) == False:
        return jsonify({"message": "invalid skill id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "uUnauthorized"}), 403

    skill_data = db.session.query(Skill).filter(
        Skill.skill_id == skill_id).first()

    if skill_data:
        db.session.delete(skill_data)
        db.session.commit()

        return jsonify({"message":'Skill deleted'}), 200

    return jsonify({"message":'You don\'t have this skill'}), 404

#activity skill
@authenticate_return_auth
def skill_activity(req: Request, skill_id, auth_info) -> Response:
    if not validate_uuid4(skill_id):
        return jsonify({"message": "invalid skill id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        skill_data = db.session.query(Skill).filter(Skill.skill_id == skill_id).first()

    if skill_data:
        skill_data.active = not skill_data.active
        db.session.commit()

        return jsonify({"message": "skill activity updated", "skill": skill_schema.dump(skill_data)}), 200
    return jsonify({"message": "You don't have this skill"}), 404
