from flask import request, Response, Blueprint

import controller

contact = Blueprint('contact', __name__)

#create
@contact.route("/contact", methods=["POST"])
def contact_add():
    return controller.contact_add(request)

#read-all
@contact.route("/contact", methods=["GET"])
def contact_get_all():
    return controller.contact_get_all(request)

#read-one
@contact.route("/contact/<contact_name>", methods=["GET"])
def contact_get_by_contact_name(contact_name):
    return controller.contact_get_by_contact_name(request, contact_name)

#update
@contact.route("/contact/<contact_name>", methods=["PUT"])
def contact_update(contact_name):
    return controller.contact_update(request, contact_name)

#delete
@contact.route("/contact/delete/<contact_id>", methods=["DELETE"])
def contact_delete(contact_id):
    return controller.contact_delete(request, contact_id)

#archive
@contact.route("/contact/archive/<contact_id>", methods=["PATCH"])
def contact_archive(contact_id):
    return controller.contact_archive(request, contact_id)



