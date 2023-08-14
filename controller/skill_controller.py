from flask import jsonify, Request, Response
from db import db
from util.reflection import populate_object
from model.skill import Skill, skill_schema, skills_schema


#create skill
def skill_add(req: Request) -> Response:
    post_data = req.get_json()
    if post_data:
        skill_name = post_data.get('skill_name')
        skill_use = post_data.get('skill_use')
        active = post_data.get("active")
        new_skill = Skill.get_new_skill()
        populate_object(new_skill, post_data)
        db.session.add(new_skill)
        db.session.commit()
        return jsonify({"message": "skill created", "skill": skill_schema.dump(new_skill)}), 201
    return jsonify({"message": 'no data'}), 404

#read skill one
def skill_get_by_id(req: Request, skill_id) -> Response:
    skill_id = skill_id.strip()
    skill_data = db.session.query(Skill).filter(
        Skill.skill_id == skill_id).first()
    if skill_data:
        skill_dict = skill_schema.dump(skill_data)
        return jsonify([skill_dict]), 200
    return jsonify({"message":'You do not have this skill'}), 404

#read all
def skill_get_all(req: Request) -> Response:
    all_skills = db.session.query(Skill).all()
    skill_list = skills_schema.dump(all_skills)
    return jsonify(skill_list), 200

#update skill
def skill_update(req: Request, skill_id) -> Response:
    post_data = req.get_json()
    if post_data:
        skill_name = post_data.get('skill_name')
        skill_use = post_data.get('skill_use')
        active = post_data.get("active")
        skill_data = db.session.query(Skill).filter(
            Skill.skill_id == skill_id).first()
        populate_object(skill_data, post_data)
        db.session.commit()
        return jsonify({"message": "skill updated", "skill": skill_schema.dump(skill_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete skill
def skill_delete(req: Request, skill_id) -> Response:
    skill_data = db.session.query(Skill).filter(
        Skill.skill_id == skill_id).first()
    if skill_data:
        db.session.delete(skill_data)
        db.session.commit()
        return jsonify({"message":'Skill deleted'}), 200
    return jsonify({"message":'You don\'t have this skill'}), 404

#archive skill
def skill_archive(req: Request, skill_id) -> Response:
    skill_data = db.session.query(Skill).filter(Skill.skill_id == skill_id).first()
    if skill_data:
        skill_data.active = not skill_data.active
        db.session.commit()
        return jsonify({"message": "skill archive updated", "skill": skill_schema.dump(skill_data)}), 200
    return jsonify({"message": "You don't have this skill"}), 404
