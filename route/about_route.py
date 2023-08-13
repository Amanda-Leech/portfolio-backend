from flask import request, Response, Blueprint

import controller

about = Blueprint('about', __name__)

#create
@about.route("/about", methods=["POST"])
def about_add() -> Response:
    return controller.about_add(request)

#read-one
@about.route("/about/<about_title>", methods=["GET"])
def about_get_by_title(about_title):
    return controller.about_get_by_title(request, about_title)

#read-all
@about.route("/about", methods=["GET"])
def about_get_all():
    return controller.about_get_all(request)

#update
@about.route("/about/<about_title>", methods=["POST"])
def about_update(about_title):
    return controller.about_update(request, about_title)

#delete
@about.route("/about/delete/<about_id>", methods=["DELETE"])
def about_delete(about_id):
    return controller.about_delete(request, about_id)

#archive
@about.route("/about/archive/<about_id>", methods=["PATCH"])
def about_archive(about_id):
    return controller.about_archive(request, about_id)
