from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma

from db import db


class Message(db.Model):
    __tablename__ = "Message"
    message_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    Message_name = db.Column(db.String())
    Message_email = db.Column(db.String() nullable=False)
    Message_subject = db.Column(db.String())
    Message = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, message_name, message_email, message_subject, message, active=True):
        self.message_name = message_name
        self.message_email = message_email
        self.message_subject= message_subject
        self.message = message
        self.active = active

    def get_new_message():
        return Message("", "", "", "", True)


class MessageSchema(ma.Schema):
    class Meta:
        fields = ['message_id', 'message_name', 'message_email', 'message_subject', 'message', 'active']


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
