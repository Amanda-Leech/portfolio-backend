from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.message import Message, message_schema, messages_schema


#create message
def message_add(req: Request) -> Response:
    post_data = req.get_json()

    if post_data:
        message_name = post_data.get('message_name')
        message_email = post_data.get('message_email')
        message_subject = post_data.get('message_subject')
        message = post_data.get("message")
        address = post_data.get("address")
        active = post_data.get("active")

        # if auth_info.user.role not in ["admin"]:
        #     return jsonify({"message": "not authorized"}), 401

        # if not message_email:
        #     return jsonify({"message" : "Email required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        new_message = Message.get_new_message()

        populate_object(new_message, post_data)

        db.session.add(new_message)
        db.session.commit()

        return jsonify({"message": "message created", "message": message_schema.dump(new_message)}), 201
    return jsonify({"message": 'no data'}), 404

#read message one
def message_get_by_id(req: Request, message_id) -> Response:
    message_id = message_id.strip()

    if validate_uuid4(message_id) == False:
        return jsonify({"message": "invalid message id"}), 400

    message_data = db.session.query(Message).filter(
        Message.message_id == message_id).first()

    if message_data:
        message_dict = message_schema.dump(message_data)

        return jsonify([message_dict]), 200

    return jsonify({"message":'You do not have this message'}), 404

#read all
# @authenticate_return_auth
def message_get_all(req: Request) -> Response:
    all_messages = db.session.query(Message).all()
    message_list = messages_schema.dump(all_messages)

    # if auth_info.user.role not in ["admin"]:
    #     return jsonify({"message": "unauthorized"}), 401

    return jsonify(message_list), 200

#update message
@authenticate_return_auth
def message_update(req: Request, message_id, auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        message_name = post_data.get('message_name')
        message_email = post_data.get('message_email')
        message_subject = post_data.get('message_subject')
        message = post_data.get("message")
        address = post_data.get("address")
        active = post_data.get("active")

        if validate_uuid4(message_id) == False:
            return jsonify({"message": "invalid message id"}), 400

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "unauthorized"}), 401

        message_data = db.session.query(Message).filter(
            Message.message_id == message_id).first()
        
        if bool(message_email):
            if message_name== "":
                return jsonify({"message" : "Email required"}), 400
          
        if not message_data:
            return jsonify({"message": "message not found"}), 404

        if message_id:
            if not validate_uuid4(message_id):
                return jsonify({"message": "invalid message id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(message_data, post_data)
        db.session.commit()

        return jsonify({"message": "message updated", "message": message_schema.dump(message_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete message
@authenticate_return_auth
def message_delete(req: Request, message_id, auth_info) -> Response:
    if validate_uuid4(message_id) == False:
        return jsonify({"message": "invalid message id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "uUnauthorized"}), 403

    message_data = db.session.query(Message).filter(
        Message.message_id == message_id).first()

    if message_data:
        db.session.delete(message_data)
        db.session.commit()

        return jsonify({"message":'Message deleted'}), 200

    return jsonify({"message":'You don\'t have this message'}), 404

#archive message
@authenticate_return_auth
def message_archive(req: Request, message_id, auth_info) -> Response:
    if not validate_uuid4(message_id):
        return jsonify({"message": "invalid message id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        message_data = db.session.query(Message).filter(Message.message_id == message_id).first()

    if message_data:
        message_data.active = not message_data.active
        db.session.commit()

        return jsonify({"message": "message archive updated", "message": message_schema.dump(message_data)}), 200
    return jsonify({"message": "You don't have this message"}), 404
