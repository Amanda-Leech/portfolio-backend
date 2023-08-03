import functools
from flask import Response
from datetime import datetime

from db import db

from model.auth import Auth

from util.validate_uuid4 import validate_uuid4


def validate_auth(arg_zero):
    auth = arg_zero.headers["auth"]

    if not auth or not validate_uuid4(auth):
        return False

    try:
        auth_record = db.session.query(
            Auth
        ).filter(
            Auth.auth == auth
        ).filter(
            Auth.expiration > datetime.utcnow()
        ).first()

        return auth_record
    except:
        return False


def failure_response():
    return Response("Authentication Required", 401)


def authenticate(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        auth_info = validate_auth(args[0])

        return (
            func(
                *args, **kwargs
            )

            if auth_info else failure_response()
        )

    return wrapper_authenticate


def authenticate_return_auth(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        auth_info = validate_auth(args[0])
        kwargs["auth_info"] = auth_info

        return (
            func(
                *args, **kwargs
            )

            if auth_info else failure_response()
        )

    return wrapper_authenticate
