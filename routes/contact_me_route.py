from flask import request, Response, Blueprint

import controllers

contact_me = Blueprint('contact_me', __name__)

#create
@contact_me.route("/contact_me", methods=["POST"])
def contact_me_add() -> Response:
    return controllers.contact_me_add(request)

#read-all
@contact_me.route("/contact_me", methods=["GET"])
def contact_me_get_all():
    return controllers.contact_me_get_all(request)

#read-one
@contact_me.route("/contact_me/<contact_me_id>", methods=["GET"])
def contact_me_get_by_id(contact_me_id):
    return controllers.contact_me_get_by_id(request, contact_me_id)

#update
@contact_me.route("/contact_me/<contact_me_id>", methods=["PUT"])
def contact_me_update(contact_me_id):
    return controllers.contact_me_update(request, contact_me_id)

#delete
@contact_me.route("/contact_me/delete/<contact_me_id>", methods=["DELETE"])
def contact_me_delete(contact_me_id):
    return controllers.contact_me_delete(request, contact_me_id)

#activity
@contact_me.route("/contact_me/activity/<contact_me_id>", methods=["PATCH"])
def contact_me_activity(contact_me_id):
    return controllers.contact_me_activity(request, contact_me_id)



