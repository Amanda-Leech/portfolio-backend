from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Contact(db.Model):
    __tablename__ = "Contact"
    contact_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    contact_name = db.Column(db.String(), nullable=False)
    linked_in = db.Column(db.String())
    git_hub = db.Column(db.String())
    phone = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    address = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, contact_name, linked_in, git_hub, phone, email, address, active=True):
        self.contact_name = contact_name
        self.linked_in = linked_in
        self.git_hub = git_hub
        self.phone = phone
        self.email = email
        self.address = address
        self.active = active

    def get_new_contact():
        return Contact("", "","","","", "", True)


class ContactSchema(ma.Schema):
    class Meta:
        fields = ['contact_id', 'contact_name', 'linked_in', 'git_hub', 'phone', 'email', 'address', 'active']


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
