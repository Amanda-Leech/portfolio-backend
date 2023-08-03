from flask import request, Response, Blueprint

import controller

resume = Blueprint('resume', __name__)

#create
@resume.route("/resume", methods=["POST"])
def resume_add() -> Response:
    return controller.resume_add(request)

#read-one
@resume.route("/resume/<resume_id>", methods=["GET"])
def resume_get_by_id(resume_id):
    return controller.resume_get_by_id(request, resume_id)

#read-search
@resume.route("/resume/search", methods=["GET"])
def resume_get_by_search():
    return controller.resume_get_by_search(request)

#read-all
@resume.route("/resume", methods=["GET"])
def resume_get_all():
    return controller.resume_get_all(request)

#update
@resume.route("/resume/<resume_id>", methods=["PUT"])
def resume_update(resume_id):
    return controller.resume_update(request, resume_id)

#delete
@resume.route("/resume/delete/<resume_id>", methods=["DELETE"])
def resume_delete(resume_id):
    return controller.resume_delete(request, resume_id)

#activity
@resume.route("/resume/activity/<resume_id>", methods=["PATCH"])
def resume_activity(resume_id):
    return controller.resume_activity(request, resume_id)


