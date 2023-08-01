from flask import request, Response, Blueprint

import controllers

education = Blueprint('education', __name__)

#create
@education.route("/education", methods=["POST"])
def education_add() -> Response:
    return controllers.education_add(request)

#read-all
@education.route("/education", methods=["GET"])
def education_get_all():
    return controllers.education_get_all(request)

#read-one
@education.route("/education/<education_id>", methods=["GET"])
def education_get_by_id(education_id):
    return controllers.education_get_by_id(request, education_id)

#read-search
@education.route("/education/search", methods=["GET"])
def education_get_by_search():
    return controllers.education_get_by_search(request)

#update
@education.route("/education/<education_id>", methods=["PUT"])
def education_update(education_id):
    return controllers.education_update(request, education_id)

#delete
@education.route("/education/delete/<education_id>", methods=["DELETE"])
def education_delete(education_id):
    return controllers.education_delete(request, education_id)

#activity
@education.route("/education/activity/<education_id>", methods=["PATCH"])
def education_activity(education_id):
    return controllers.education_activity(request, education_id)

