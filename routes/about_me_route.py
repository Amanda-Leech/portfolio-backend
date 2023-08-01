from flask import request, Response, Blueprint

import controllers

about_me = Blueprint('about_me', __name__)

#create
@about_me.route("/about_me", methods=["POST"])
def about_me_add() -> Response:
    return controllers.about_me_add(request)

#read-all
@about_me.route("/about_me", methods=["GET"])
def about_me_get_all():
    return controllers.about_me_get_all(request)

#read-one
@about_me.route("/about_me/<about_me_id>", methods=["GET"])
def about_me_get_by_id(about_me_id):
    return controllers.about_me_get_by_id(request, about_me_id)

#update
@about_me.route("/about_me/<about_me_id>", methods=["PUT"])
def about_me_update(about_me_id):
    return controllers.about_me_update(request, about_me_id)

#delete
@about_me.route("/about_me/delete/<about_me_id>", methods=["DELETE"])
def about_me_delete(about_me_id):
    return controllers.about_me_delete(request, about_me_id)

#activity
@about_me.route("/about_me/activity/<about_me_id>", methods=["PATCH"])
def about_me_activity(about_me_id):
    return controllers.about_me_activity(request, about_me_id)
