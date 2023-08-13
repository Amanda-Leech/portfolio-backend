from flask import jsonify, Request, Response
from datetime import datetime, timedelta

from db import db

from lib.authenticate import authenticate_return_auth

from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object

from model.contact import Contact, contact_schema, contacts_schema


#create contact
@authenticate_return_auth
def contact_add(req: Request,auth_info) -> Response:
    post_data = req.get_json()

    if post_data:
        contact_name = post_data.get('contact_name')
        linked_in = post_data.get('linked_in')
        git_hub = post_data.get('git_hub')
        phone = post_data.get("phone")
        email = post_data.get("email")
        address = post_data.get("address")
        active = post_data.get("active")

        if auth_info.user.role not in ["admin"]:
            return jsonify({"message": "not authorized"}), 401

        if not contact_name or not phone or not email:
            return jsonify({"message" : "Name, phone and email required"}), 400

        if active and active not in [True, False]:
            return jsonify({"error": "invalid"}), 400

        new_contact = Contact.get_new_contact()

        populate_object(new_contact, post_data)

        db.session.add(new_contact)
        db.session.commit()

        return jsonify({"message": "contact created", "contact": contact_schema.dump(new_contact)}), 201
    return jsonify({"message": 'no data'}), 404

#read contact one
def contact_get_by_contact_name(req: Request, contact_name) -> Response:
    contact_name = contact_name.strip()

    # if validate_uuid4(contact_id) == False:
    #     return jsonify({"message": "invalid contact id"}), 400

    contact_data = db.session.query(Contact).filter(
        Contact.contact_name == contact_name).first()

    if contact_data:
        contact_dict = contact_schema.dump(contact_data)

        return jsonify([contact_dict]), 200

    return jsonify({"message":'You do not have this contact'}), 404

#read all
def contact_get_all(req: Request) -> Response:
    all_contacts = db.session.query(Contact).all()
    contact_list = contacts_schema.dump(all_contacts)

    return jsonify({"message": "success", "contacts": contact_list}), 200

#update contact
# @authenticate_return_auth
def contact_update(req: Request, contact_name) -> Response:
    post_data = req.get_json()

    if post_data:
        contact_name = post_data.get('contact_name')
        linked_in = post_data.get('linked_in')
        git_hub = post_data.get('git_hub')
        phone = post_data.get("phone")
        email = post_data.get("email")
        address = post_data.get("address")
        active = post_data.get("active")

        # if validate_uuid4(contact_id) == False:
        #     return jsonify({"message": "invalid contact id"}), 400

        # if auth_info.user.role not in ["admin"]:
        #     return jsonify({"message": "unauthorized"}), 401

        contact_data = db.session.query(Contact).filter(
            Contact.contact_name == contact_name).first()
        
        if bool(phone)==False or bool(email)==False:
            if contact_name== "" or phone == "" or email == "":
                return jsonify({"message" : "Name, phone and email required"}), 400
          
        if not contact_data:
            return jsonify({"message": "contact not found"}), 404

        # if contact_id:
        #     if not validate_uuid4(contact_id):
        #         return jsonify({"message": "invalid contact id"}), 400

        if active and type(active) != bool:
            return jsonify({"message": "please provide a valid active value"}), 400

        populate_object(contact_data, post_data)
        db.session.commit()

        return jsonify({"message": "contact updated", "contact": contact_schema.dump(contact_data)}), 200
    return jsonify({"message": "no data"}), 404

#delete contact
@authenticate_return_auth
def contact_delete(req: Request, contact_id, auth_info) -> Response:
    if validate_uuid4(contact_id) == False:
        return jsonify({"message": "invalid contact id"}), 400

    if auth_info.user.role != "admin":
        return jsonify({"message": "uUnauthorized"}), 403

    contact_data = db.session.query(Contact).filter(
        Contact.contact_id == contact_id).first()

    if contact_data:
        db.session.delete(contact_data)
        db.session.commit()

        return jsonify({"message":'Contact deleted'}), 200

    return jsonify({"message":'You don\'t have this contact'}), 404

#archive contact
@authenticate_return_auth
def contact_archive(req: Request, contact_id, auth_info) -> Response:
    if not validate_uuid4(contact_id):
        return jsonify({"message": "invalid contact id"}), 400

    if auth_info.user.role not in ["admin"]:
        return jsonify({"message": "not authorized"}), 401

    if auth_info.user.role in ['admin']:
        contact_data = db.session.query(Contact).filter(Contact.contact_id == contact_id).first()

    if contact_data:
        contact_data.active = not contact_data.active
        db.session.commit()

        return jsonify({"message": "contact archive updated", "contact": contact_schema.dump(contact_data)}), 200
    return jsonify({"message": "You don't have this contact"}), 404
