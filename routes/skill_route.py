from flask import request, Response, Blueprint

import controllers

skill = Blueprint('skill', __name__)

#create
@skill.route("/skill", methods=["POST"])
def skill_add() -> Response:
    return controllers.skill_add(request)

#read-all
@skill.route("/skill", methods=["GET"])
def skill_get_all():
    return controllers.skill_get_all(request)

#read-one
@skill.route("/skill/<skill_id>", methods=["GET"])
def skill_get_by_id(skill_id):
    return controllers.skill_get_by_id(request, skill_id)

#read-search
@skill.route("/skill/search", methods=["GET"])
def skill_get_by_search():
    return controllers.skill_get_by_search(request)

#update
@skill.route("/skill/<skill_id>", methods=["PUT"])
def skill_update(skill_id):
    return controllers.skill_update(request, skill_id)

#delete
@skill.route("/skill/delete/<skill_id>", methods=["DELETE"])
def skill_delete(skill_id):
    return controllers.skill_delete(request, skill_id)

#activity
@skill.route("/skill/activity/<skill_id>", methods=["PATCH"])
def skill_activity(skill_id):
    return controllers.skill_activity(request, skill_id)

