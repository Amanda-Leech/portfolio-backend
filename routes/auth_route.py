from flask import request, Response, Blueprint

from controllers import auth_controller as controller

auth = Blueprint("auth", __name__)


@auth.route("/user/auth", methods=["POST"])
def auth_token_add():
    return controller.auth_token_add(request)


@auth.route("/user/logout", methods=["DELETE"])
def auth_token_remove():
    return controller.auth_token_remove(request)



