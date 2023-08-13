from flask import request, Response, Blueprint
# import validate_auth from "..lib/authenticate"
from controller import auth_controller as controller
from lib import authenticate as lib

auth = Blueprint("auth", __name__)


    
@auth.route("/auth", methods=["GET"])
def auth_get():
    return controller.auth_get(request)


@auth.route("/user/auth", methods=["POST"])
def auth_add():
    return controller.auth_add(request)


@auth.route("/user/logout", methods=["DELETE"])
def auth_remove():
    return controller.auth_remove(request)



