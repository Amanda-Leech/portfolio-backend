from flask import request, Response, Blueprint

import controllers

cover_page = Blueprint('cover_page', __name__)

#create
@cover_page.route("/cover_page", methods=["POST"])
def cover_page_add() -> Response:
    return controllers.cover_page_add(request)

#read-all
@cover_page.route("/cover_page", methods=["GET"])
def cover_page_get_all():
    return controllers.cover_page_get_all(request)

#read-one
@cover_page.route("/cover_page/<cover_page_id>", methods=["GET"])
def cover_page_get_by_id(cover_page_id):
    return controllers.cover_page_get_by_id(request, cover_page_id)

#update
@cover_page.route("/cover_page/<cover_page_id>", methods=["PUT"])
def cover_page_update(cover_page_id):
    return controllers.cover_page_update(request, cover_page_id)

#delete
@cover_page.route("/cover_page/delete/<cover_page_id>", methods=["DELETE"])
def cover_page_delete(cover_page_id):
    return controllers.cover_page_delete(request, cover_page_id)

#activity
@cover_page.route("/cover_page/activity/<cover_page_id>", methods=["PATCH"])
def cover_page_activity(cover_page_id):
    return controllers.cover_page_activity(request, cover_page_id)

