from flask import request, Response, Blueprint

import controller

about = Blueprint('about', __name__)

#create
@about.route("/about", methods=["POST"])
def about_add() -> Response:
    return controller.about_add(request)

#read-one
@about.route("/about/<about_id>", methods=["GET"])
def about_get_by_id(about_id):
    return controller.about_get_by_id(request, about_id)

#read-all
@about.route("/about", methods=["GET"])
def about_get_all():
    return controller.about_get_all(request)

#update
@about.route("/about/<about_id>", methods=["PUT"])
def about_update(about_id):
    return controller.about_update(request, about_id)

#delete
@about.route("/about/delete/<about_id>", methods=["DELETE"])
def about_delete(about_id):
    return controller.about_delete(request, about_id)

#archive
@about.route("/about/archive/<about_id>", methods=["PATCH"])
def about_archive(about_id):
    return controller.about_archive(request, about_id)
