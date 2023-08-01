from flask import request, Response, Blueprint

import controllers

project = Blueprint('project', __name__)

#create
@project.route("/project", methods=["POST"])
def project_add() -> Response:
    return controllers.project_add(request)

#read-all
@project.route("/project", methods=["GET"])
def project_get_all():
    return controllers.project_get_all(request)

#read-one
@project.route("/project/<project_id>", methods=["GET"])
def project_get_by_id(project_id):
    return controllers.project_get_by_id(request, project_id)

#read-search
@project.route("/project/search", methods=["GET"])
def project_get_by_search():
    return controllers.project_get_by_search(request)

#update
@project.route("/project/<project_id>", methods=["PUT"])
def project_update(project_id):
    return controllers.project_update(request, project_id)

#delete
@project.route("/project/delete/<project_id>", methods=["DELETE"])
def project_delete(project_id):
    return controllers.project_delete(request, project_id)

#activity
@project.route("/project/activity/<project_id>", methods=["PATCH"])
def project_activity(project_id):
    return controllers.project_activity(request, project_id)

