from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Contact_me(db.Model):
    __tablename__ = "Contact_me"
    contact_me_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    contact_name = db.Column(db.String(), nullable=False, unique=True)
    linked_in = db.Column(db.String())
    git_hub = db.Column(db.String())
    phone = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, contact_name, linked_in, git_hub, phone, email, active=True):
        self.contact_name = contact_name
        self.linked_in = linked_in
        self.git_hub = git_hub
        self.phone = phone
        self.email = email
        self.active = active

    def get_new_contact():
        return Contact_me("", "","","","", True)


class ContactSchema(ma.Schema):
    class Meta:
        fields = ['contact_me_id', 'contact_name', 'linked_in', 'git_hub', 'phone', 'email', 'active']


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
