from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.project import Project, project_schema, projects_schema


#create project
@authenticate_return_auth
def project_add(req: Request,auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        project_url = post_data.get('project_url')
        project_title = post_data.get('project_title')
        project_info = post_data.get('project_info')
        project_id = post_data.get("project_id")
        git_url = post_data.get("git_url")
        active = post_data.get("active")

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "not authorized"}), 401

        if not project_title:
            return jsonify({"message" : "Project title required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        if project_id:
            if not validate_uuid4(project_id):
                return jsonify({"message": 'not a valid project id'}), 400

            new_project = Project.get_new_project()

            populate_object(new_project, post_data)

            db.session.add(new_project)
            db.session.commit()

            return jsonify({"message": "project created", "project": project_schema.dump(new_project)}), 201
        return jsonify({"message": "Project id needed"}), 400
    return jsonify({"message": 'no data'}), 404

#read project one
def project_get_by_id(req: Request, project_id) -> Response:
    project_id = project_id.strip()

    if validate_uuid4(project_id) == False:
        return jsonify({"message": "invalid project id"}), 400

    project_data = db.session.query(Project).filter(
        Project.project_id == project_id).first()

    if project_data:
        project_dict = project_schema.dump(project_data)

        return jsonify({"message": "success", "project": project_dict}), 200

    return jsonify({"message":'You do not have this project'}), 404

#read search
def project_get_by_search(req: Request) -> Response:
    project_search = req.args.get('q').lower()

    project_query = db.session.query(Project).filter(Project.project_id == Project.project_id)\
        .filter(db.or_(
            db.func.lower(Project.project_info).contains(project_search),
            db.func.lower(Project.project_title).contains(project_search)
        )).all()

    return jsonify({"message": "projects found", "projects": projects_schema.dump(project_query)}), 200

#read all
def project_get_all(req: Request) -> Response:
    all_projects = db.session.query(Project).all()
    project_list = projects_schema.dump(all_projects)

    return jsonify({"message": "success", "projects": project_list}), 200

#update project
@authenticate_return_auth
def project_update(req: Request, project_id, auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        project_url = post_data.get('project_url')
        project_title = post_data.get('project_title')
        project_info = post_data.get('project_info')
        project_id = post_data.get("project_id")
        git_url = post_data.get("git_url")
        active = post_data.get("active")

        if validate_uuid4(project_id) == False:
            return jsonify({"message": "invalid project id"}), 400

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "unauthorized"}), 401

        project_data = db.session.query(Project).filter(
            Project.project_id == project_id).first()
        
        if bool(project_title)==False:
            if project_title == "":
                return jsonify({"message" : "Project name required"}), 400
          
        if not project_data:
            return jsonify({"message": "Project not found"}), 404

        if project_id:
            if not validate_uuid4(project_id):
                return jsonify({"message": "Invalid project id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(project_data, post_data)
        db.session.commit()

        return jsonify({"message": "project updated", "project": project_schema.dump(project_data)}), 200
    return jsonify({"message": "no project"}), 404

#delete project
@authenticate_return_auth
def project_delete(req: Request, project_id, auth_info) -> Response:
    if validate_uuid4(project_id) == False:
        return jsonify({"message": "invalid project id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    project_data = db.session.query(Project).filter(
        Project.project_id == project_id).first()

    if project_data:
        db.session.delete(project_data)
        db.session.commit()

        return jsonify({"message":'Project deleted'}), 200

    return jsonify({"message":'You don\'t have this project'}), 404

#activity project
@authenticate_return_auth
def project_activity(req: Request, project_id, auth_info) -> Response:
    if not validate_uuid4(project_id):
        return jsonify({"message": "invalid project id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        project_data = db.session.query(Project).filter(Project.project_id == project_id).first()

    if project_data:
        project_data.active = not project_data.active
        db.session.commit()

        return jsonify({"message": "project activity updated", "project": project_schema.dump(project_data)}), 200
    return jsonify({"message": "You don't have this project"}), 404
