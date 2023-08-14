from flask import jsonify, Request, Response
from db import db
from util.reflection import populate_object
from model.contact import Contact, contact_schema, contacts_schema

#create contact
def contact_add(req: Request) -> Response:
    post_data = req.get_json()
    if post_data:
        contact_name = post_data.get('contact_name')
        linked_in = post_data.get('linked_in')
        git_hub = post_data.get('git_hub')
        phone = post_data.get("phone")
        email = post_data.get("email")
        address = post_data.get("address")
        active = post_data.get("active")
        new_contact = Contact.get_new_contact()
        populate_object(new_contact, post_data)
        db.session.add(new_contact)
        db.session.commit()
        return jsonify([contact_schema.dump(new_contact)]), 201
    return jsonify({"message": 'no data'}), 404

#read contact one
def contact_get_by_contact_name(req: Request, contact_name) -> Response:
    contact_name = contact_name.strip()
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
    return jsonify([contact_list]), 200

#update contact
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
        contact_data = db.session.query(Contact).filter(
            Contact.contact_name == contact_name).first()
        if not contact_data:
            return jsonify({"message": "contact not found"}), 404
        populate_object(contact_data, post_data)
        db.session.commit()
        return jsonify([contact_schema.dump(contact_data)]), 200
    return jsonify({"message": "no data"}), 404

#delete contact
def contact_delete(req: Request, contact_id) -> Response:
    contact_data = db.session.query(Contact).filter(
        Contact.contact_id == contact_id).first()
    if contact_data:
        db.session.delete(contact_data)
        db.session.commit()
        return jsonify({"message":'Contact deleted'}), 200
    return jsonify({"message":'You don\'t have this contact'}), 404

#archive contact
def contact_archive(req: Request, contact_id) -> Response:
    contact_data = db.session.query(Contact).filter(Contact.contact_id == contact_id).first()
    if contact_data:
        contact_data.active = not contact_data.active
        db.session.commit()
        return jsonify({contact_schema.dump(contact_data)}), 200
    return jsonify({"message": "You don't have this contact"}), 404
