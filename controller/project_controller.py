from flask import jsonify, Request, Response
from db import db
from util.reflection import populate_object
from model.project import Project, project_schema, projects_schema


#create project
def project_add(req: Request) -> Response:
    post_data = req.get_json()
    if post_data:
        project_url = post_data.get('project_url')
        project_title = post_data.get('project_title')
        project_info = post_data.get('project_info')
        git_url = post_data.get("git_url")
        active = post_data.get("active")
        if not project_title:
            return jsonify({"message" : "Project title required"}), 400
        new_project = Project.get_new_project()
        populate_object(new_project, post_data)
        db.session.add(new_project)
        db.session.commit()
        return jsonify([project_schema.dump(new_project)]), 201
    return jsonify({"message": 'no data'}), 404

#read project one
def project_get_by_id(req: Request, project_id) -> Response:
    project_id = project_id.strip()
    project_data = db.session.query(Project).filter(
        Project.project_id == project_id).first()
    if project_data:
        project_dict = project_schema.dump(project_data)
        return jsonify([project_dict]), 200
    return jsonify({"message":'You do not have this project'}), 404

#read all
def project_get_all(req: Request) -> Response:
    all_projects = db.session.query(Project).all()
    project_list = projects_schema.dump(all_projects)
    return jsonify(project_list), 200

#update project
def project_update(req: Request, project_id) -> Response:
    post_data = req.get_json()
    if post_data:
        project_url = post_data.get('project_url')
        project_title = post_data.get('project_title')
        project_info = post_data.get('project_info')
        git_url = post_data.get("git_url")
        active = post_data.get("active")
        project_data = db.session.query(Project).filter(
            Project.project_id == project_id).first()
        populate_object(project_data, post_data)
        db.session.commit()
        return jsonify([project_schema.dump(project_data)]), 200
    return jsonify({"message": "no project"}), 404

#delete project
def project_delete(req: Request, project_id) -> Response:
    project_data = db.session.query(Project).filter(
        Project.project_id == project_id).first()
    if project_data:
        db.session.delete(project_data)
        db.session.commit()
        return jsonify({"message":'Project deleted'}), 200
    return jsonify({"message":'You don\'t have this project'}), 404

#archive project
def project_archive(req: Request, project_id) -> Response:
    project_data = db.session.query(Project).filter(Project.project_id == project_id).first()
    if project_data:
        project_data.active = not project_data.active
        db.session.commit()
        return jsonify([project_schema.dump(project_data)]), 200
    return jsonify({"message": "You don't have this project"}), 404
