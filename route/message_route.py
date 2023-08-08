from flask import request, Response, Blueprint

import controller

message = Blueprint('message', __name__)

#create
@message.route("/message", methods=["POST"])
def message_add() -> Response:
    return controller.message_add(request)

#read-all
@message.route("/message", methods=["GET"])
def message_get_all():
    return controller.message_get_all(request)

#read-one
@message.route("/message/<message_id>", methods=["GET"])
def message_get_by_id(message_id):
    return controller.message_get_by_id(request, message_id)

#delete
@message.route("/message/delete/<message_id>", methods=["DELETE"])
def message_delete(message_id):
    return controller.message_delete(request, message_id)

#archive
@message.route("/message/archive/<message_id>", methods=["PATCH"])
def message_archive(message_id):
    return controller.message_archive(request, message_id)



