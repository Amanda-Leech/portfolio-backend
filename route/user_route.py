from flask import request, Response, Blueprint

import controller

user = Blueprint('user', __name__)

#create
@user.route("/user", methods=["POST"])
def user_add() -> Response:
    return controller.user_add(request)

#read-all
@user.route("/user", methods=["GET"])
def user_get_all():
    return controller.user_get_all(request)

#read-one
@user.route("/user/<user_id>", methods=["GET"])
def user_get_by_id(user_id):
    return controller.user_get_by_id(request, user_id)

#update
@user.route("/user/<user_id>", methods=["PUT"])
def user_update(user_id):
    return controller.user_update(request, user_id)

#delete
@user.route("/user/delete/<user_id>", methods=["DELETE"])
def user_delete(user_id):
    return controller.user_delete(request, user_id)

#archive
@user.route("/user/archive/<user_id>", methods=["PATCH"])
def user_archive(user_id):
    return controller.user_archive(request, user_id)

