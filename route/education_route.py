from flask import request, Response, Blueprint

import controller

education = Blueprint('education', __name__)

#create
@education.route("/education", methods=["POST"])
def education_add() -> Response:
    return controller.education_add(request)

#read-all
@education.route("/education", methods=["GET"])
def education_get_all():
    return controller.education_get_all(request)

#read-one
@education.route("/education/<education_id>", methods=["GET"])
def education_get_by_id(education_id):
    return controller.education_get_by_id(request, education_id)

#update
@education.route("/education/<education_id>", methods=["PUT"])
def education_update(education_id):
    return controller.education_update(request, education_id)

#delete
@education.route("/education/delete/<education_id>", methods=["DELETE"])
def education_delete(education_id):
    return controller.education_delete(request, education_id)

#activity
@education.route("/education/activity/<education_id>", methods=["PATCH"])
def education_activity(education_id):
    return controller.education_activity(request, education_id)

