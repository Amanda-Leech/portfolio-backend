from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db
from .user import UserSchema


class Auth(db.Model):
    __tablename__ = "Auth"
    auth = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)
    now_datetime = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", back_populates="auth")

    def __init__(self, user_id, expiration, now_datetime):
        self.user_id = user_id
        self.expiration = expiration
        self.now_datetime = now_datetime


def get_new_auth():
    return Auth("", "", "")
class AuthSchema(ma.Schema):
    class Meta:
        fields = ['auth', 'user', 'expiration', 'now_datetime']

    user = ma.fields.Nested(UserSchema(only=("role", "email", "user_id", "active")))


auth_schema = AuthSchema()
auths_schema = AuthSchema(many=True)
