from flask import request, Response, Blueprint

import controller

contact = Blueprint('contact', __name__)

#create
@contact.route("/contact", methods=["POST"])
def contact_add() -> Response:
    return controller.contact_add(request)

#read-all
@contact.route("/contact", methods=["GET"])
def contact_get_all():
    return controller.contact_get_all(request)

#read-one
@contact.route("/contact/<contact_id>", methods=["GET"])
def contact_get_by_id(contact_id):
    return controller.contact_get_by_id(request, contact_id)

#update
@contact.route("/contact/<contact_id>", methods=["PUT"])
def contact_update(contact_id):
    return controller.contact_update(request, contact_id)

#delete
@contact.route("/contact/delete/<contact_id>", methods=["DELETE"])
def contact_delete(contact_id):
    return controller.contact_delete(request, contact_id)

#archive
@contact.route("/contact/archive/<contact_id>", methods=["PATCH"])
def contact_archive(contact_id):
    return controller.contact_archive(request, contact_id)



