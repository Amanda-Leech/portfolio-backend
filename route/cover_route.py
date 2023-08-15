from flask import request, Response, Blueprint

import controller

cover = Blueprint('cover', __name__)

#create
@cover.route("/cover", methods=["POST"])
def cover_add() -> Response:
    return controller.cover_add(request)

#read-one
@cover.route("/cover/<cover_title>", methods=["GET"])
def cover_get_by_cover_title(cover_title):
    return controller.cover_get_by_cover_title(request, cover_title)

@cover.route("/cover/id/<cover_id>", methods=["GET"])
def cover_get_by_id(cover_id):
    return controller.cover_get_by_id(request, cover_id)

#read-all
@cover.route("/cover", methods=["GET"])
def cover_get_all():
    return controller.cover_get_all(request)

#update
@cover.route("/cover/<cover_title>", methods=["PUT"])
def cover_update(cover_title):
    return controller.cover_update(request, cover_title)

#delete
@cover.route("/cover/delete/<cover_id>", methods=["DELETE"])
def cover_delete(cover_id):
    return controller.cover_delete(request, cover_id)

#archive
@cover.route("/cover/archive/<cover_id>", methods=["PATCH"])
def cover_archive(cover_id):
    return controller.cover_archive(request, cover_id)

