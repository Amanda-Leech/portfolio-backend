from flask import jsonify, Request, Response
from flask_bcrypt import generate_password_hash
from db import db
from model.user import User, user_schema, users_schema
from model.auth import Auth, auth_schema
from lib.authenticate import authenticate_return_auth, authenticate

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object


def verify_role(user_data, auth_info):
    if auth_info.user.role == 'admin' and user_data.role == 'admin':
        return True
    else:
        return False


@authenticate_return_auth
def user_add(req: Request, auth_info) -> Response:
    post_data = req.get_json()
    role = post_data.get("role")
    email = post_data.get("email")
    password = post_data.get("password")
    active = post_data.get("active")

    if role:
        if role not in ['admin']:
            return jsonify({"message": "invalid role"}), 400

    if active:
        if active not in [True, False]:
            return jsonify({"message": "invalid active value"}), 400

    # if email and password:
    #     if ' ' in password:
    #         return jsonify({'message': 'invalid password'}), 403

        duplicate_email = db.session.query(User).filter(User.email == email).first()
        if duplicate_email == None:
            new_user = User.get_new_user()

            populate_object(new_user, post_data)

            new_user.password = generate_password_hash(new_user.password).decode("utf8")

            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "user created", "user": user_schema.dump(new_user)}), 201

        else:
            return jsonify({"message": "email not available"}), 400

    else:
        return jsonify({"message": "email and password required"}), 400


@authenticate
def user_get_by_id(req: Request, user_id) -> Response:
    user_id = user_id.strip()

    if validate_uuid4(user_id) == False:
        return jsonify({"message": "invalid id"}), 400

    user_data = db.session.query(User).filter(User.user_id == user_id).first()

    return jsonify({"message": "user results", "user": user_schema.dump(user_data)})


@authenticate_return_auth
def user_get_from_auth_token(req: Request, auth_info) -> Response:
    return jsonify({"message": "auth user found", "auth_token": auth_schema.dump(auth_info)}), 200


@authenticate
def user_get_all(req: Request) -> Response:
    all_users = db.session.query(User).all()

    return jsonify({"message": "user results", "users": users_schema.dump(all_users)})


@authenticate_return_auth
def user_update(req: Request, user_id, auth_info) -> Response:
    post_data = req.get_json()
    role = post_data.get("role")
    email = post_data.get("email")
    password = post_data.get("password")
    active = post_data.get("active")

    validate_user_id = validate_uuid4(user_id)

    if not validate_user_id:
        return jsonify({"message": "invalid id"}), 400

    if password != None:
        if ' ' in password:
            return jsonify({'message': 'invalid password'}), 403

        post_data['password'] = generate_password_hash(
            post_data["password"]).decode("utf8")

    if active:
        if active not in [True, False]:
            return jsonify({"message": "invalid active value"}), 400

    user_data = db.session.query(User).filter(User.user_id == user_id).first()

    if user_data:
        if user_data.active == True or active == True:
            if auth_info.user.role != 'admin' and user_data.role == 'admin':
                return jsonify({"message": "admins cannot update admins"}), 401

            if email:
                if email.lower() != user_data.email:
                    duplicate_email = db.session.query(User).filter(User.email == email).first()
                    if duplicate_email != None:
                        return jsonify({"message": "email is already in use"}), 400

            populate_object(user_data, post_data)

            db.session.commit()

            return jsonify({"message": "user updated", "user": user_schema.dump(user_data)}), 200
        else:
            return jsonify({"message": "user inactive"}), 400
    else:
        return jsonify({"message": "user not found"}), 404


@authenticate_return_auth
def user_delete(req: Request, user_id, auth_info) -> Response:
    if validate_uuid4(user_id) == False:
        return jsonify({"message": "invalid id"}), 400

    if auth_info.user.user_id == user_id:
        return jsonify({"message": "user cannot delete themself"}), 403

    if auth_info.user.role != 'admin':
        return jsonify({"message": "forbidden - admins cannot delete users"}), 403

    user_data = db.session.query(User).filter(User.user_id == user_id).first()

    if user_data:
        db.session.delete(user_data)
        db.session.commit()

        return jsonify({"message": 'user deleted'}), 200

    return jsonify({"message": 'user not found'}), 404


@authenticate_return_auth
def user_archive(req: Request, user_id, auth_info) -> Response:
    if validate_uuid4(user_id) == False:
        return jsonify({"message": "invalid id"}), 400

    if auth_info.user.role in ['admin']:
        user_data = db.session.query(User).filter(User.user_id == user_id).first()

        if user_data:

            if user_data.user_id == auth_info.user.user_id:
                return jsonify({"message": "user cannot change their own active status"}), 403

            user_data.active = not user_data.active

            db.session.commit()

            return jsonify({"message": "user active status updated", "user": user_schema.dump(user_data)}), 200

        else:
            return jsonify({"message": 'user not found'}), 404

    else:
         if auth_info.user.role == 'user':
                return jsonify({"message": "unauthorized"}), 401
