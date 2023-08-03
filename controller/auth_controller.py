from flask import jsonify, Response, Request
from datetime import datetime, timedelta
import base64
import uuid
from flask_bcrypt import check_password_hash, generate_password_hash
from db import db
from util.validate_uuid4 import validate_uuid4
from lib.authenticate import authenticate_return_auth
from model.auth import Auth, auth_schema
from model.user import User, user_schema

auto_login_token_clean = True

def auth_add(req: Request) -> Response:
    if req.content_type == "application/json":
        post_data = req.get_json()
        email = post_data.get("email")
        password = post_data.get("password")

        if not email or not password:
            return jsonify({"message": "Try again"}), 400

        now_datetime = datetime.utcnow()
        expiration_datetime = datetime.utcnow() + timedelta(hours=12)
        user_data = db.session.query(User).filter(User.email == email).filter(User.active).first()

        if user_data:
            if user_data.active == False:
                return jsonify({"message": "inactive"}), 403

            is_password_valid = check_password_hash(user_data.password, password)

            if is_password_valid == False:
                return jsonify({"message": "invalid email/password"}), 401

            if auto_login_token_clean:
                auth = db.session.query(Auth).filter(Auth.user_id == user_data.user_id).filter(Auth.expiration < now_datetime).all()

                for token in auth:
                    db.session.delete(token)

            auth_data = Auth(user_data.user_id, expiration_datetime)
            db.session.add(auth_data)

        else:
            return jsonify({"message": "invalid login"}), 401

        db.session.commit()
        return jsonify({"message": "auth success", "auth info": auth_schema.dump(auth_data), "user info": user_schema.dump(user_data)})

    else:
        return jsonify({"message": "ERROR: request must be made in JSON format"}), 400


@authenticate_return_auth
def auth_remove(req: Request, auth_info) -> Response:
    if req.content_type == "application/json":
        try:
            db.session.delete(auth_info)
            db.session.commit()

            return jsonify("User logged out"), 200
        except:
            return jsonify("Could not delete session"), 500
    else:
        return jsonify({"message": "request must be in JSON format"}), 400

